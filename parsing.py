from module import *

# parsing artikel
def parsingnews(url):
    # membuat request
    r = requests.get(url)
    # hasil responts
    request = r.content
    # BeautifulSoup soup inisialisasi
    soup = BeautifulSoup(request, 'html.parser')

    # menyimpan dalam bentuk list
    teks_prod = []

    # menemukan tag artikel halaman lama
    # teks = soup.find_all('div', attrs={'class':'detail_text'})

    # menemukan tag artikel pada halaman baru
    teks = soup.findAll('p', attrs={'class':''})

    # loop setiap tag <p></p> pada artikel
    for x in range(0, len(teks)):
        kalimat = teks[x].text.strip()
        teks_prod.append(kalimat)
        text = " ".join(str(x) for x in teks_prod)
        textnews = re.sub(r"(ADVERTISEMENT)|(ADVERTISEMENT SCROLL TO RESUME CONTENT)|(SCROLL TO RESUME CONTENT)|([Gambas:Video CNN])","", text)

    # mengembalikan nilai textnews
    return textnews