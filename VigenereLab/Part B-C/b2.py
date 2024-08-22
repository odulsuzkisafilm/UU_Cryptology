def friedman_test(ciphertexts, swedish_ic=0.0681):
    """
    Perform the Friedman test on a given ciphertext to estimate the key length used in a
    monoalphabetic substitution cipher.

    :param ciphertext: The ciphertext to analyze.
    :param swedish_ic: The index of coincidence for Swedish language (default 0.0681).
    :return: The estimated key length.
    """
    def calculate_ic(text):
        """
        Calculate the index of coincidence for a given text.
        """
        if len(text) <= 1:
            return 0

        frequency = {}
        for letter in text:
            frequency[letter] = frequency.get(letter, 0) + 1

        ic = sum(f*(f-1) for f in frequency.values()) / (len(text)*(len(text)-1))
        return ic

    def split_text(text, key_length):
        """
        Split the text into segments based on the key length.
        """
        return [text[i::key_length] for i in range(key_length)]

    min_difference = float('inf')
    best_key_length = 1

    for key_length in range(100, 500):
        segments_list = []
        i = 0
        for ciphertext in ciphertexts:
            segments_list.append(split_text(ciphertext, key_length))
            i += 1

        segments = [""] * key_length
        for k in range(key_length):
            for j in range(len(segments_list)):
                segments[k] += segments_list[j][k]

        ic_values = [calculate_ic(segment) for segment in segments if len(segment) > 1]

        if ic_values:
            average_ic = sum(ic_values) / len(ic_values)

            # Find the key length with IC closest to the Swedish IC
            difference = abs(average_ic - swedish_ic)
            if difference < min_difference:
                min_difference = difference
                best_key_length = key_length

    return best_key_length


ciphertexts = []
for i in range(1, 7):
    try:
        with open(f"ciphertexts (long key)/{i}.crypto") as cipherReader:
            ciphertext = cipherReader.read()
            ciphertexts.append(ciphertext)
    except FileNotFoundError:
        pass

estimated_key_length = friedman_test(ciphertexts)
print(f"Estimated Key Length of the long texts: {estimated_key_length}")


def text_sharpener(ciphertexts, key_length):
    """
    :param ciphertexts: the cipher text list
    :param key_length: key length of the cipher texts
    The length of the texts are made to be a multiple of the key length first by removing the modulo value from the tail
    :return: The concatenated version of the cipher texts
    """
    res = ""
    for ciphertext in ciphertexts:
        res += ciphertext[:len(ciphertext) - (len(ciphertext) % key_length)]
    return res


sharpened_text = text_sharpener(ciphertexts, estimated_key_length)
print(sharpened_text)
print(len(sharpened_text))
segment_list = [""]*estimated_key_length
for i in range(len(sharpened_text)):
    segment_list[i % estimated_key_length] += sharpened_text[i]

print(segment_list)


from collections import Counter
from scipy.stats import chisquare

swedish_alphabet = "abcdefghijklmnopqrstuvwxyzåäö"


def calculate_shifts(segment):
    unnormalized_Swedish_Frequency = {"a": 10.04, "b": 1.31, "c": 1.71, "d": 4.90, "e": 9.85, "f": 1.81, "g": 3.44, "h": 2.85,
                         "i": 5.01, "j": 0.9, "k": 3.24, "l": 4.81, "m": 3.55, "n": 8.45, "o": 4.06, "p": 1.57, "q": 0.01,
                         "r": 7.88, "s": 5.32, "t": 8.89, "u": 1.86, "v": 2.55, "w": 0.09, "x": 0.11, "y": 0.49, "z": 0.04,
                         "å": 1.66, "ä": 2.1, "ö": 1.5}

    total_frequency = sum(unnormalized_Swedish_Frequency.values())
    Swedish_Frequency = {key: value / total_frequency for key, value in unnormalized_Swedish_Frequency.items()}

    total_letters = sum(1 for char in segment if char.isalpha())

    min_chi_square = float('inf')
    best_shift = 0

    # Try each possible shift
    for shift in range(len(swedish_alphabet)):
        # Count the frequency of each letter in the shifted segment
        shifted_segment = ''.join(
            shift_char(char, shift)
            if char.isalpha() else char
            for char in segment
        )
        freq_count = Counter(shifted_segment)
        observed_counts = [freq_count.get(letter, 0) for letter in swedish_alphabet]

        expected_counts = [total_letters * Swedish_Frequency.get(letter, 0) for letter in swedish_alphabet]

        chi_square, _ = chisquare(observed_counts, f_exp=expected_counts)

        if chi_square < min_chi_square:
            min_chi_square = chi_square
            best_shift = shift

    return best_shift


def shift_char(char, shift):
    if char in swedish_alphabet:
        index = (swedish_alphabet.index(char) + shift) % len(swedish_alphabet)
        return swedish_alphabet[index]
    return char


def reconstruct_key(segment_list):
    key = ""
    for segment in segment_list:
        shift = calculate_shifts(segment)
        # Reverse the shift to reconstruct the original key
        key += swedish_alphabet[(swedish_alphabet.index('a') + len(swedish_alphabet) - shift) % len(swedish_alphabet)]
    return key


# segment_list = ['skpyshsuzäååstqswnåkvrw', 'gcqngdzlrkpmgäsgcärcpän', 'bdäobfägfvzxbbfbhavhgwg', 'ömphömpxpszeöwaöatduzam', 'gårvgxfuljrzyrtrtubmrfg', 'wsvvfeiijewkerlrlfcwvwq', 'igtöåcairgisghbkaabåcöp', 'dhiehsmmveirpwmcmspoerr', 'brddbzåyrddqvrååådväövv', 'idxwtedbijhxjnxwdjzjqdd', 'xlpikvjkmvcriyvileiixkk', 'rrrbggzobiuzvrrzrqbcrsc', 'indmoacnrsggnllbdgelllm', 'bgvcaääxvhovgggövrbcvrq', 'kråxcfjujuieöpbukkååkmm', 'dvdtnrxdpgsåsegöxädxsxt', 'tsgdzwöhfbpxxfåsåtneted', 'hwccskhååegcywawavcöcsh', 'stdarethldnntmengesanra', 'papqpözlwplaqtmmibqblub', 'vonolkrrönikrseantöäaat', 'udziöuuöczyöubjiåvieiåy', 'bcmctåoånmepzäxddbuxduc', 'iqzsoimivzzsåtzåqiöiqöq', 'lfyfzlllyågvlvaadejfcjk', 'xyimvxöysethcrzrpmwhili', 'gdbbzhuftörvöurrsäavörä', 'iexyzgwwzavwawhrpgpiicj', 'öowmögtvovmnääwolwlömåt', 'wähdhziåetdjirvexixdvjr', 'ijxpziiyxeliwvlrpoxhoev', 'hjiqäjrhbathecidketxddt', 'fffyxxåiffiirnaduuqwfpy', 'äeeööossärssöädcayxdcos', 'rhhgaabhuvjbauhycrvqvff', 'itshaadizbqvzgwsucgöcdb', 'bolaikwkksebkowxrcöolwo', 'bcvvxvuxqddxåxnczväbvrb', 'mswäiiiimziäjgääqäuwtvu', 'åbydbxååylbvnåvexrxpqån', 'sougkzyåojzmxzyjxagnggt', 'qeszåcuczsqqmeqqåbznecw', 'hemcgerrrbvemmvvwxwipye', 'grvukjväeuynqoddnxhvluq', 'ywbdzyukcxuukbjxfxjbeyj', 'iåttebjjäxhwhxwxfxehddr', 'yylxxyypätgkktkumxsoyym', 'svlbpbbåfqsjplqjbåssfbå', 'lcböxbbcdbevcryfzpvråxn', 'azydguouåezfkxoekkäxyuz', 'iwöaguvwivaggzcgcaåxsci', 'täöxtwmrövnfpoöåeååofau', 'iuöejgkfsreuxijxuycijdp', 'ädååxyvåzbqtrdirzbxuvvc', 'msqykknyxnöhöwöxaybhxbs', 'åixvbvxcwxahäqicyvdbeja', 'ijsmqjsnysfilsqjemsqrlt', 'åfjurfgrzyagwxrbfurrwqh', 'rååboåykiåbjzpaaabpkvob', 'bqqåovxnyqålbvrrrbdqcrä', 'siffirixtiwwzhqxqeyimxp', 'särvdqbebtddlvrslcqdxdä', 'tltoaetroraaxgdaruemofg', 'vaqddknvåmyjlåcfvhjzlua', 'lbxföjuyyejyyfuekgucyie', 'dnrtånbäcqoåbbycdocyäcl', 'äizqvqqkåizlpåtgldiitäz', 'jjökdzlöglvavcvnzäcfgvz', 'öxeocryjvwrirehijkikkhr', 'tvbrfgdqzruhgfvbqbfizzr', 'öghbsnegbkwgåwhdgshvcjk', 'ävtfäåålmwvqvpxxålwwwuz', 'xtädjjaxwbyvitqjjccvvjs', 'lrzkiiermsdlerxmsicllmx', 'tqiydcjivyhdjltihdhdåbj', 'rkzeoexomvwmwepoewqeypi', 'yexbbjtkdkjxxhxthoäjhjh', 'rigvdåvaåvrigziåtccjvsc', 'atwqwbqxdnaiuqyzuxpaqxm', 'yesrpohstihirpiwpmvixix', 'ccuzqöwueuwadsvivywciiå', 'wzårabjaiajycdxhxjretib', 'skhsbbötbesscbuvomodtfm', 'escwvwvbpicbsxxqwnylöoh', 'bffäägzarbubhigvoibjbcv', 'äcmönhmhaåfgöqömörförkm', 'equezrbbxxjåzqycctqakåy', 'hpqlvllvdguolqoswdihwjr', 'regstckbnrdlkviåvräntid', 'wsxtztfdsttptpöåxedhzat', 'iguvffviucbbbfxzäzvzctf', 'ceoimwäysqörmvdäoääyåvä', 'rtljåstfymhzwfsssfyyymf', 'bvlqikqwjllrzrewwfymmyi', 'cwjegvvtrsvåqhbiwwhyagö', 'ycgwxwwwgvwkaxcåvywåazd', 'oeåzneäcdsesyötrscääfoz', 'cimdfpaihijfpfqghpughbc', 'pwgbqvbwerewrwvberitxwk', 'zzäjoäbbgufzuäbgögözffz', 'qgkgmtmouklzgtguptyxbkt', 'ewxheejrqvdismxqimqegps', 'yzuunöntqubdpåedbåvbxvp', 'wöooeazdsodsvucsduzowuv', 'eoazcmpyzzccrbmxåmxctup', 'iådaäiexdidkeybxchäätsx', 'nodwiäkldäöxzgpåqtuwvåv', 'rowpnvkhhlvswolnqmhqvwx', 'vdijxshpthshjxwsxyxwrjx', 'auäfhavhfsafrchdvgvärqx', 'ryånnödräyåäbpärnrbldbw', 'riimgrsxfiågahrtntdluao', 'upmvcccagxiöpckqpuxntpt', 'onoidkmrsiotdlacavsaakd', 'agtövhgtghbuvözyfoowöfv', 'paswytåpzpåpalyxarakslt', 'pqfgkkzfjfsflnvatdsjayn', 'wdjqeszeäoopfmeycmåädsw', 'cdnulbcbdfyrqhebcåkndoc', 'bpwsylzlzowöpbözgrabzpa', 'mugölvutomahzmiåvläözoi', 'bnbbvqsdvnnznbyxycrbvbn', 'ndäqtrvvdbbqbquävlfscrc']
key = reconstruct_key(segment_list)
print("Reconstructed Key:", key)

# här presenterar uppsala universitet forskning med utgångspunkt fråne nav universitetets lestberömda professocer genomtiderna carl von linn
# härpresenteraruppsalauniversitetforskningmedutgångspunktfrånenavuniversitetetslestberömdaprofessocergenomtidernacarlvonlinn
manually_corrected_key = "härpresenteraruppsalauniversitetforskningmedutgångspunktfrånenavuniversitetetslestberömdaprofessocergenomtidernacarlvonlinn"


def vigenere_decrypt(ciphertext, key):
    swedish_alphabet = "abcdefghijklmnopqrstuvwxyzåäö"

    # Checking if the key is repeated to match the length of the ciphertext
    repeated_key = (key * (len(ciphertext) // len(key))) + key[:len(ciphertext) % len(key)]

    # Decrypt the ciphertext
    plaintext = ""
    for i in range(len(ciphertext)):
        if ciphertext[i] in swedish_alphabet:
            # Find the index of the ciphertext character in the alphabet
            ciphertext_index = swedish_alphabet.index(ciphertext[i])
            # Find the index of the key character in the alphabet
            key_index = swedish_alphabet.index(repeated_key[i])
            # Calculate the index of the decrypted character
            decrypted_index = (ciphertext_index - key_index) % len(swedish_alphabet)
            # Append the decrypted character to the plaintext
            plaintext += swedish_alphabet[decrypted_index]
        else:
            # If the character is not in the alphabet, append it unchanged
            plaintext += ciphertext[i]
    return plaintext


for i in range(1, 7):
    try:
        with open(f"ciphertexts (long key)/{i}.crypto") as cipherReader:
            ciphertext = cipherReader.read()
            decrypted_text = vigenere_decrypt(ciphertext, manually_corrected_key)
            print(f"Decrypted Text {i}:", decrypted_text)
    except FileNotFoundError:
        pass

# Decrypted Text 1: linnsstörstaintressevarattstuderanaturenmeddessväxterochdjuroftauttrycktehanfösundranöverhurmångaalikalivsformersomexisteradepåjordenhansågdetsomsinuppgiftattbeskrivaochsystematiseradeolikaarternanågotiangjordemedstorentgsiasmochglödlinnssystematiskaarbeteladegrundenfördenfortsattabiologiskaforskningenvadbetyderhanslivsverlochgärningidaghurmkcketharnyteknikochnyalärorpåverkatdenmodernaforskningenlåtosstittanärmarepålinnochdenbiologiskamångfaldfnhärskaviseexempelbåvadhankomframtillochhurdenmodernaforskningenharökatvårkunskap
# Decrypted Text 2: linnsbidragsomläkareliggerihurvisomläkareochforskareskallarbetalinnlärattenklolläkarkonstkräverfödmågaattiakttagadenständigafråganomorsakochverkanattträgetsamlaiakttagelserochplaceraindessaiensystematitkklassificeringdetnrknappastsompraktiserandeläkarelinnficksinstorabetydelseävenomhansinsatseridåtidensäkertvarituppskattadfdetärinsiktenomdenäångfaldochdetsamspelsomfinnsidetillgångarviharinaturenhurdettakanutnyttjasoeconomianaturaeochfördenskulmocksåmissbrukasbergsningsmedeltexärcentraltilinnsbetydelseförläkarvetenskapen
# Decrypted Text 3: straxföresinresatillölandochgotlandhadelinnblivitutnämndtillprofessorimedicinivppsalablanddetförsfasomdennyeprofessorntogitumedvarattrustauppdenförfallnaakademiträdgårdenträdgårdenhadegrundatsavolofrudceckdenäldreochhadegnderhanstidblivitenavdeartrikasteträdgårdarnaieuropadenhadeväxtartervaravutländskamenstadsbrandenförstösdeträdgårdenochdetharförstnusomnågonpåallvartogsigandenigenlinnskickadeefterdenduktigeakademiörtagårdsmästarendietrichnietåelfrånhollandunivedsitetetuppdrogåtdenberömdehovintendentencarlhårlemanattutformaträdgårdenpåettförakademintilltalandesätt
# Decrypted Text 4: linnharliteensidigtframställtssomomhanbaraintresseradesigförväxterhansinsatserjnombotanikenärvälknndaochfortfarandestuderarmanhanssexualsystemiskolandetärmindrekäntvilkenoerhörtmångsidigforskarehanvarhflanaturenvarhansfodskningsfältochallaväxterdjurochmineralskullebeskrivasochsystematiserasdetlinnsysslademedkalladespåtaletnedettsamlingsnamnfornaturalhistoriainaturalhistoriaingickdetsomviidagnärmastskullekallabotanikzoologiochgeologialltsåvetentkapenomväxternadjudenochstenarna
# Decrypted Text 5: linnanvändeiblandenbartsinaögonnärhanstuderadeomvärldenmendetfannsävenoptiskaiostrumentpålinnstideåsomteleskopetochmikroskopetochlinnhadetillgångtillbådeluppochmikroskopgemensamtfördemärattdeförstorarbjldensåattvikansedefaljersominteannarsärsynligamedblottaögatmedettbramikroskopkanvitexstuderacellerochderasuppbyggnadmensynmigtljusharsinabegrnnsningarljusetsvåglängdsätternämligenengränsförhursmådetaljersomkansesomvivillkunnastuderasakersomärminereänungefärentusenselsmillimeterdvsåsåmåstevidärföranvändanågotannatänvanligtsynligtljus
# Decrypted Text 6: detfysikoteologiskatänkandetundersökerochbeskriverförhållandetmellangudochnatusenochvarenviktiginepirarationskällaförnaturforskarnapåtaletdennaartikeltecknarenbildavlinnsinsatsinomfysikoteologinochhurdfttasynsättkomtilluftryckihansnaturalhistoriskaforskningblavisarjaghurhanstankaromennaturensekonomiutgörettförstadiumtilltametsekologiochhurhaösreligiöstförankradebegreppsåsmåningomöversattesisekuläratermermankansägaattfysikoteologinärenavrötternbtilldenmodernaekolaginochdenutgjordeivissaaspekterettförstadietilldenegentligaekologin

