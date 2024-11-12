import requests

#------------------------------Question 1.1------------------------------
print("------------------------------Question 1.1------------------------------")
N = 143516336909281815529104150147210248002789712761086900059705342103220782674046289232082435789563283739805745579873432846680889870107881916428241419520831648173912486431640350000860973935300056089286158737579357805977019329557985454934146282550582942463631245697702998511180787007029139561933433550242693047924440388550983498690080764882934101834908025314861468726253425554334760146923530403924523372477686668752567287060201407464630943218236132423772636675182977585707596016011556917504759131444160240252733282969534092869685338931241204785750519748505439039801119762049796085719106591562217115679236583
e = 3
C = 1101510739796100601351050380607502904616643795400781908795311659278941419415375

# Function to compute the integer cube root
def integer_cube_root(n):
    low = 0
    high = n
    while low <= high:
        mid = (low + high) // 2
        mid_cubed = mid ** 3
        if mid_cubed == n:
            return mid
        elif mid_cubed < n:
            low = mid + 1
        else:
            high = mid -1
    return high

M = integer_cube_root(C)

# Verify that M^e == C
assert M ** 3 == C, "Failed to find the correct cube root of C"

# Convert integer message back to plaintext
def int_to_bytes(M):
    M_bin_str = bin(M)[2:]  # Remove '0b' prefix
    padding = (8 - len(M_bin_str) %8) %8
    M_bin_str = '0' * padding + M_bin_str
    bytes_list = [M_bin_str[i:i+8] for i in range(0, len(M_bin_str),8)]
    bytes_int = [int(b,2) for b in bytes_list]
    # Construct bytes object and decode using UTF-8
    bytes_array = bytes(bytes_int)
    plaintext = bytes_array.decode('utf-8', errors='replace')
    return plaintext

plaintext = int_to_bytes(M)
print("Le message déchiffré est:", plaintext)
#Le message déchiffré est: Umberto Eco

#------------------------------Question 1.2------------------------------
print("------------------------------Question 1.2------------------------------")
# Function to convert a string to a list of integers (UTF-8 codes)
def str_to_int_list(x):
    z = [ord(a) for a in x]
    return z

# Function to convert a string to an integer by concatenating the binary representations
def str_to_int(x):
    x_list = str_to_int_list(x)
    res = ""
    for a in x_list:
        ci = "{:08b}".format(a)
        res = res + ci
    res = int(res, 2)
    return res

# Function to convert an integer back to a string
def int_to_str(n):
    bits = bin(n)[2:]
    # Pad bits to be a multiple of 8
    while len(bits) % 8 != 0:
        bits = '0' + bits
    res = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        res += chr(int(byte, 2))
    return res

def reformat_name(name):
    if ',' in name:
        last, first = name.split(',', 1)
        return first.strip() + ' ' + last.strip()
    return name

def convert_name_format(names):
    return [reformat_name(name) for name in names]


# Function to search for the author page by page from the Gutendex API
def search_author_page_by_page():
    url = "https://gutendex.com/books/"
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}")
        if response.status_code == 200:
            data = response.json()
            authors = [author['name'] for book in data['results'] for author in book['authors']]
            authors = convert_name_format(authors)


            # Iterate over the current page's authors to find a match
            for author in authors:
                m_candidate = str_to_int(author)
                C_candidate = pow(m_candidate, e, N)
                if C_candidate == C:
                    return author  # return the author's name when found

            # Check if there are more pages
            if data['next'] is None:
                break
            page += 1
        else:
            print("Failed to retrieve data from the API.")
            break
    return None
# Clé publique Question 1.2
N = 172219604291138178634924980176652297603347655313304280071646410523864939208855547078498922947475940487766894695848119416017067844129458299713889703424997977808694983717968420001033168722360067307143390485095229367172423195469582545920975539060699530956357494837243598213416944408434967474317474605697904676813343577310719430442085422937057220239881971046349315235043163226355302567726074269720408051461805113819456513196492192727498270702594217800502904761235711809203123842506621973488494670663483187137290546241477681096402483981619592515049062514180404818608764516997842633077157249806627735448350463
e = 173

# Cryptogramme 1.2
C = 25782248377669919648522417068734999301629843637773352461224686415010617355125387994732992745416621651531340476546870510355165303752005023118034265203513423674356501046415839977013701924329378846764632894673783199644549307465659236628983151796254371046814548224159604302737470578495440769408253954186605567492864292071545926487199114612586510433943420051864924177673243381681206265372333749354089535394870714730204499162577825526329944896454450322256563485123081116679246715959621569603725379746870623049834475932535184196208270713675357873579469122917915887954980541308199688932248258654715380981800909

# Search for the author page by page
author = search_author_page_by_page()
if author:
    print("Le message déchiffré est:")
    print(author)
    #Le message déchiffré est: Marcel Proust

    # Optionally, verify the result
    print("\n------------------------------Vérification 1.2------------------------------:")
    m_candidate = str_to_int(author)
    C_candidate = pow(m_candidate, e, N)
    print("Candidat C =", C_candidate)
    print("C fourni   =", C)
    print("Candidat C == C fourni:", C_candidate == C)
else:
    print("L'auteur n'a pas été trouvé.")
