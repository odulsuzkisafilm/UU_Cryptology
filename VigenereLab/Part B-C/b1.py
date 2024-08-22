def friedman_test(ciphertext, swedish_ic=0.0681):
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

    # Test for key lengths from 1 to 16
    for key_length in range(1, 17):
        segments = split_text(ciphertext, key_length)
        ic_values = [calculate_ic(segment) for segment in segments if len(segment) > 1]
        if ic_values:
            average_ic = sum(ic_values) / len(ic_values)

            # Find the key length with IC closest to the Swedish IC
            difference = abs(average_ic - swedish_ic)
            if difference < min_difference:
                min_difference = difference
                best_key_length = key_length

    return best_key_length


key_lengths = []
cipher_texts = []
for i in range(1, 26):
    try:
        with open(f"ciphertexts (short key)/vig_group{i}.crypto") as cipherReader:
            ciphertext = cipherReader.read()
            cipher_texts.append(ciphertext)
            estimated_key_length = friedman_test(ciphertext)
            print(f"Estimated Key Length of {i}'th group: {estimated_key_length}")
            key_lengths.append(estimated_key_length)
    except FileNotFoundError:
        pass

print(key_lengths)

segment_matrix = [[]] * len(key_lengths)
for i in range(len(segment_matrix)):
    segment_matrix[i] = ["" for k in range(key_lengths[i])]
    for j in range(len(cipher_texts[i])):
        segment_matrix[i][j % key_lengths[i]] += cipher_texts[i][j]

print()
print(segment_matrix)


from collections import Counter
from scipy.stats import chisquare

swedish_alphabet = "abcdefghijklmnopqrstuvwxyzåäö"

def calculate_shifts(segment):
    # The expected frequencies of letters in the Swedish language
    unnormalized_Swedish_Frequency = {"a": 10.04, "b": 1.31, "c": 1.71, "d": 4.90, "e": 9.85, "f": 1.81, "g": 3.44, "h": 2.85,
                         "i": 5.01, "j": 0.9, "k": 3.24, "l": 4.81, "m": 3.55, "n": 8.45, "o": 4.06, "p": 1.57, "q": 0.01,
                         "r": 7.88, "s": 5.32, "t": 8.89, "u": 1.86, "v": 2.55, "w": 0.09, "x": 0.11, "y": 0.49, "z": 0.04,
                         "å": 1.66, "ä": 2.1, "ö": 1.5}

    total_frequency = sum(unnormalized_Swedish_Frequency.values())
    Swedish_Frequency = {key: value / total_frequency for key, value in unnormalized_Swedish_Frequency.items()}

    total_letters = sum(1 for char in segment if char.isalpha())

    min_chi_square = float('inf')
    best_shift = 0

    # Trying each possible shift
    for shift in range(len(swedish_alphabet)):
        # Counting the frequency of each letter in the shifted segment
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
        # Reversing the shift to reconstruct the original key
        key += swedish_alphabet[(swedish_alphabet.index('a') + len(swedish_alphabet) - shift) % len(swedish_alphabet)]
    return key


print()
keys = []
for i in range(len(segment_matrix)):
    key = reconstruct_key(segment_matrix[i])
    print(f"{i + 1}th Reconstructed Key:", key)
    keys.append(key)

# 1st Reconstructed Key: fettsvörnyckel
# 2nd Reconstructed Key: dansdrottningen
# 3rd Reconstructed Key: åqxrlbeopwnciakm
# 4th Reconstructed Key: datavetare
# 5th Reconstructed Key: dunderhonung
# 6th Reconstructed Key: öåcykelnyckelåä
# 7th Reconstructed Key: notsorandom
# 8th Reconstructed Key: vidskeplig
# 9th Reconstructed Key: barbieflotte
# 10th Reconstructed Key: smärtfsitt
# 11th Reconstructed Key: cryptology
# 12th Reconstructed Key: tjolahopp
# 13th Reconstructed Key: invöåpzuaboztjvm
# 14th Reconstructed Key: datainspeksionen
# 15th Reconstructed Key: sannolikhet
# 16th Reconstructed Key: lyckatill
# 17th Reconstructed Key: bellmwn
# 18th Reconstructed Key: sannolikhet


# # Manually Adjusted Keys:
# 1-) fettsvårnyckel
# 2-) dansdrottningen
# 3-) åqxrlbeopwnciakm
# 4-) datavetare
# 5-) dunderhonung
# 6-) öåcykelnyckelåä
# 7-) notsorandom
# 8-) vidskeplig
# 9-) barbieflotte
# 10-) smärtfritt
# 11-) cryptology
# 12-) tjolahopp
# 13-) invöåpzuabozljvm
# 14-) datainspektionen
# 16-) sannolikhet
# 18-) lyckatill
# 19-) bellman
# 25-) sannolikhet


manually_adjusted_keys = ["fettsvårnyckel", "dansdrottningen", "åqxrlbeopwnciakm", "datavetare", "dunderhonung", "öåcykelnyckelåä", "notsorandom", "vidskeplig", "barbieflotte", "smärtfritt", "cryptology", "tjolahopp", "invöåpzuabozljvm", "datainspektionen", "sannolikhet", "lyckatill", "bellman", "sannolikhet"]

def vigenere_decrypt(ciphertext, key):
    # Make sure the key is repeated to match the length of the ciphertext
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


print()
j = 0
for i in range(1, 26):
    try:
        with open(f"ciphertexts (short key)/vig_group{i}.crypto") as cipherReader:
            ciphertext = cipherReader.read()
            decrypted_text = vigenere_decrypt(ciphertext, manually_adjusted_keys[j])
            j += 1
            print(f"Decrypted Text for the group {i}:", decrypted_text)
    except FileNotFoundError:
        pass


# Decrypted Text for the group 1: härkommerpippilångstrumptjolahopptjolahejtjolahoppsansahärkommerpippilångstrumpjahärkommerfaktisktjaghardusettminapaminsötafinalillaapahardusettherrnilssonjahanheterfaktisktsåhardusettminvillaminvillavillekullavillavillåvillduvetavarförvillanhetersåjofördärborjupippilångstrumptjolahopptjolahejtjolahoppsansadärborjupippilångstrumpjadärborfaktisktjagdetärinteillajagharapahästochvillaenkappsäckfullmedpengarärdetocksåbraatthakomnuallavännervarendakottesomjagkännernuskavilevaloppantjolahejtjolahoppsansa
# Decrypted Text for the group 2: dukandansadukanjiveaduharsåhimlaroligtsedentjejensevadsomhänderdiggardansdrottningenfredagskvällochljusenärdämpadeletarefternågonstansattgådärdespelarrättmusikbörjarröradigduletarefterdinkungvemsomhelstkanvaradenmannennattenärungochmusikenärhögmedliterockmusikäralltokejdukännerförattdansaochnärdufårchansenrefrängduärdansdrottningenungochfinbarasjuttonårkänntaktenfråntamburinendukandansadukanjiveaduharsåhimlaroligtsedentjejensevadsomhänderdiggardansdrottningen
# Decrypted Text for the group 3: midvinternattensköldärhårdstjärnornagnistraochglimmaallasovaiensliggårddjuptundermidnattstimmamånenvandrarsintystabansnönlyservitpåfurochgransnönlyservitpåtakenendasttomtenärvakenstårdärsågråvidladgårdsdörrgråmotdenvitadrivatittarsommångavintrarförruppemotmånensskivatittarmotskogendärgranochfurdrarkringgårdensindunklamurgrubblarfastejdetlärbåtaöverenunderliggåtaförsinhandgenomskäggochhårskakarhuvudochhättanejdengåtanäralltförsvårnejjaggissarejdettaslårsomhanplägarinomkortslikaspörjandetankarbortgårattordnaochpysslagårattskötasinsyssla
# Decrypted Text for the group 4: beomförlåtelseochhonundradepåatthansomvarenkristenprästhadeettmindreförsonligtsinnelagänenvanligvärldsmänniskakarlarturförstodinteriktigtvarthonvillekommahanstodbaraochstirradepåhennemenfrusundlersadedåattdenhärgångenvardetdenkäratantekenstedtsomhadeförbrutitsigmothonomochomhonvarsårättrådigsomhanpåstodsåkundehanjuintetvivlapåatthonnulågochångradesigochavhelasinsjällängtadeefterattfåbehonomomförlåtelse
# Decrypted Text for the group 5: hejabamsestarkastärvårbamsemenhantyckerinteomattslåssdunderhonungfarmorsdunderhoungäterhanförattblistarkförståsochkommerdetenstöddigtypochgerenlitensvagettnypdåladdarbamseuppigenmeddunderhoungenhejabamsesnällastärvårbamselyckligdensomharensådanvänhejabamsestarkastärvårbamsemenhantyckerinteomattslåssdunderhonungfarmorsdunderhoungäterhanförattblistarkförståsochkommerdetenstöddigtypochgerenlitensvagettnypdåladdarbamseuppigenmeddunderhoungenhejabamsesnällastärvårbamselyckligdensomharensådanvän
# Decrypted Text for the group 6: våranuppgiftvarattbyggaensånhållbarbrosommöjligtmedpastadenskulleocksåskullevarasåbilligsommöjligteftersomallagrupperbarahadeenbudgetpåhundramiljonermenocksåsnyggvivaldeattbyggaenhängbroeftersomvitroddedenskullevarahållbarastmaterialeftersomvihadeenbudgetpåhundramiljonersåkundeviinteriktigthaalltvivillehapåbronmatrialetsomfannsattanvändavarlasagneplattorsmalaspagettirörtjockaspagettipastarörrepsmåmakaronerochstorlitenlimpistol
# Decrypted Text for the group 7: jurgenkloppharsnartgjortsittiliverpooldetbekräftarklubbeniettpressmeddelandejagförstårattdetkanvaraenchockförmångasägerhandentysketränarenjrgenkloppanslöttillliverpoolunderhöstensedandesshardenengelskastorklubbenvunnitdetmestamankanvinnadäriblandchampionsleagueochpremierleaguemenunderfredagsförmiddagenkomchockbeskedetattkloppkommerattlämnaeftersäsongen
# Decrypted Text for the group 8: närzarathustravartrettioårgammallämnadehansitthemochsjönisitthemlandsjönisitthemlandochbegavsigtillbergenhärnjöthanavsinochsinensamhetochtröttnadeintepådetpåtioårtillslutförändradesdockhanshjärtaochenmorgonsteghanuppmedgryningenhansteguppmedgryningenställdesigframförsolenochsadetilldensåhärdustorastjärnavadskulledinlyckavaraomduintehadedigtillvilkendulyseritioårhardukommitupphittillmingrottaduskullevaratröttpådittljusochdennavägutanmigminörnochminormochminormmenviväntadepådigvarjemorgontogbortdittöverflödochvälsignadedigfördet
# Decrypted Text for the group 9: atenkanidagintebeskrivassomendemokratiintemeddestandardviharidagmendäremotvaratenväldigtdemokratiskagentemotderastidochderasstandardssåhärsågatensdemokratiutpåettungefärallafriamänsomvarmedborgareiatensomocksåhadeföräldrarsomvarföddaiatenhaderösträttighetdettabetyderattungefärpersonerhaderätttillattröstaalltsåhadecaavbefolkningeniatenrättattröstaomettsamhälleidagenbartgavavdessinvånarerättenattröstaskullevialdrigkalladetlandetfördemokratisktsedanhurdekomframtillsinabeslutvargenomatträckaupphandenommanvarförförslagetdetmotsvararändåpånågotsätthurvigörnuisverigeriksdagensarbetaretryckerpåjanejvetejsenprecissomiatenräknasrösternasammanochmankolladeomjaellernejalternativetfåttmerrösternågotlitemindredemokratisktkanmantyckaärattdeskapadesenregeringsomskullefattamindrebeslutdådetskullevaraförtidskrävandeförallaröstberättigademedborgareattbehövagåochröstapåförslagkonstantmanvaldealltsåpersonergenomlottningintilldessaregeringspositioneridagskullevityckalottningärenuselideatillattbestämmavilkasomkommerkunnabestämmalagarförvårtlandeftersomattpersonernasomblevvaldakundehanollkollpåsakernadeskullebestämmamenommanserpådetfrånettannathållsåärdetändårättsådemokratisktsättattlösasituationenpåallaharlikastorchansattblivaldaingenkanfuskapånågotsätttillattblivaldgenomattmanipuleraröstertexosv
# Decrypted Text for the group 10: hejsanmammaochpappaharesåkultpårestaurangenvadäterniförrestenjaguuundrarvadniäterochvadskaniätatillefterrättdetkanskelåtergottmenjagärhemmahoskatrinochsamuelnusuckochochskatittapåsimpsonsochhaochhadetsåkultpårestaurangenhejdå
# Decrypted Text for the group 11: nejvihaickeförlitentidosstillmättmenviförslösaförmycketavdenlivetärtillräckligtlångtochävenfördestörstaverksfullbordanärvårtidriklignogblottdenisinhelhetblirvälanvändmendärdenfårflytahänivällevnadochslarvdärdenickeanvändesförnågotförnuftigtändamåldåmärkermanengångnärdenobevekligatimmenslårattdentidvarsförrinnandeman
# Decrypted Text for the group 12: närenmanljugermördarhanendelavvärldendettaärdeblekadödarsommänfelaktigtkallarsinalivalltdettakanjagintelängreståutmedattbevittnakanintefrälsningensriketamighemendiktavcliffburtonsomframförsavjameshetfieldilåtentoliveistodieavmetallica
# Decrypted Text for the group 13: kryptologikonstenattskyddainformationärcentralförsäkerkommunikationsymmetriskochasymmetriskkrypteringtillsammansmedhashfunktioneranvändsförattsäkerställakonfidentialitetochintegritetdigitalasignaturerbekräftaravsändarensäkthetochmeddelandetsoförändradestatuskvantkryptografibaseradpåkvantmekanikensprincipererbjudersäkerhetgenomskapandeavkryptonycklarochövervakningaveventuellavlyssning
# Decrypted Text for the group 14: säkerhetsagentdeltadittuppdragbörjarvidångströmslaboratorietklnollsjutrenollinspekteraområdetnärahuvudingångenochhållutkikefterdenkodadesignalenefteratthafåttsignalenbegedigdiskrettillklubbenstockendärexaktkltvåettnollnollidetbakrerummetidentifieramåletmeddenrödabokenbytkodadedokumentochavslutakommunikationenvarytterstvaksammisstänktamotagentersnärvarobekräftadåtervändsäkerttilldinbasutanattdrauppmärksamhetkodnamnorion
# Decrypted Text for the group 16: sannoliktvadetbetydervälnåtsomärliktsanningmenriktigtlikasantsomsanningärdetinteomdetärsannoliktnuharvitydligeninterådmedäktasanningarlängreutanvifårnöjaossmedsannolikhetskalkylerdetärsynddetfördomhållerlägrekvalitetänsanningardomärintelikapålitligadomblirtillexempelväldigtolikaföreochefterjagmenarföreharrisburgsåvardetjuytterstosannoliktattdetsomhändeiharrisburgskullehändamensåfortdethadehäntrakadejusannolikhetenupptillintemindreänprocentsådetvarnästansantattdethadehänt
# Decrypted Text for the group 18: sombelöningförattnilöstedetkrypterademysterietfårnihärennygåtaenbondeborpåenöochmåstetasinbåtintillmarknadenföratthandlavälframmeköperbondenenvargettfårochettkålhuvudvidbåteninserbondenatthanendastorkarroöverenavdessasakeråtgångenproblemetärattvargenochgetenintekanblilämnadesjälvadåblirgetenuppätenintehellerkanbondenlämnagetenmedkålhuvudetdåblirkålhuvudetlammetsaftonmåltidhurskabondengöraförattfåöveralltutanattnågotbliruppätet
# Decrypted Text for the group 19: sålunkavisåsmåningomfrånbacchibullerochtumultnärdödenropargrannekomditttimglasärnufulltdugubbefälldinkryckanerochduduynglinglydminlagdenskönstanymfsommotdiglerinunderarmentagtyckerduattgravenärfördjupnåvälansåtagdigdåensuptagdigsenditoenditotvåditotresådördunöjdare
# Decrypted Text for the group 25: nuärjudethärrättkrångligtförgemenemansåegentligenärdetvälingenideatthafolkomröstningomsånthärfolkiallmänhetdomtänkerförståspåsittgrovhuggnavisattdetsomhändeiharrisburgverkligenharhäntdomtardetsomensanningtalaalltidsanningbarnsavåraföräldrartillossdetfårviintesägatillvårabarnutanvimåsteläradomattalltidtalasannoliktattsägasannolikhetenhelasannolikhetenochingentingannatänsannolikhetensåattdominserattdetsomhändeiharrisburgintekanhändahäreftersomdetinteenshändedärvilkethadevaritmycketmersannoliktmedtankepåattdetvardärdethände


