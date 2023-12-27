# import module
from module import *

# parsing news articel
from parsing import parsingnews

# preprocessing text
from prepro import filtering_text

# segementation sentences
from segementation import tokenisasi

# wight term 
from vsm import *

# similarity sentences
from similarity import cosine

# textrank methode
from textrank import *

# evaluation summary
from evaluation import evaluation_rouge



# set path
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#set jenis file
ALLOWED_EXTENSIONS = set(['pdf'])
# inisialitation static folder location
STATIC_FOLDER = 'templates/assets'

# flask app
app = Flask(__name__, static_folder=STATIC_FOLDER)  


# set file eksistensi .pdf
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# convert pdf menadi teks
def converter(filename, pages=None): #inisialisasi function dengan dua parameter 
    # kondisi untuk halaman 
    if not pages: 
        pagenums = set()
    else:
        pagenums = set(pages)

    # inisialisai function
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    # membaca file
    infile = open(filename, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text # mengembalikan hasil convert pdf ke teks


# route index halaman home
@app.route('/') 
def index(): 
    return render_template('index.html') 

# route untuk upload url artikel
@app.route('/upload_news') 
def upload_news():
    return render_template('upload_news.html') 

# route untuk upload url artikel preprocessing
@app.route('/upload_news_prepro') 
def upload_news_prepro():
    return render_template('upload_news_prepro.html') 

# route untuk upload url artikel
@app.route('/upload_evaluation') 
def upload_evaluation():
    return render_template('upload_evaluation.html')

# membaca artikel online
@app.route('/convert_read_artikel', methods=['POST', 'GET'])
def convert_read_artikel():
    if request.method == 'POST':
        url = request.form['artikel']
        urltext = parsingnews(url)
        tokenisasiteks = tokenisasi(urltext)

    return render_template('read_artikel.html', textartikel = urltext, countterm = len(tokenisasiteks), tokenized=tokenisasiteks)

# Peringkasan artikel
@app.route('/convert_artikel', methods=['POST', 'GET'])
def convert_artikel():

    if request.method == 'POST':

        text = request.form['artikelnews']
        filtertext = filtering_text(text)
        tokenisasiteks = tokenisasi(filtertext)
        tfidfteks = tfidffuc(tokenisasiteks) 
        dftfidftext = dftfidf(tokenisasiteks)
        similarity = cosine(tfidfteks) 
        similaritytoarray = similarity.toarray() 
        matrik_adjencey = res_graph_adjencey(similarity)
        skor_pagerank = pagerank(matrik_adjencey) 
        pengurutan_skor = sorted_sentences(skor_pagerank, tokenisasiteks)
        
        if not request.form['numOfLines']: 
            numOfLines = 5
        else:
            numOfLines = int(request.form['numOfLines']) 
        peringkasan = summarytopn(pengurutan_skor, numOfLines) 
        
        return render_template('success_artikel.html', output_text=text, 
                                                        filtering = filtertext,
                                                        tokenized=tokenisasiteks, 
                                                        tables=[dftfidftext.to_html(classes='table table-bordered',index=False)], 
                                                        titles=dftfidftext.columns.values, 
                                                        similarity_text=similaritytoarray, 
                                                        score_pagerank=skor_pagerank, 
                                                        sorted_score=pengurutan_skor,
                                                        summary=peringkasan
                                                        )

# peringkasan tanpa preprocessing
@app.route('/convert_artikel_non', methods=['POST', 'GET'])
def convert_artikel_non():

    if request.method == 'POST':

        text = request.form['artikelnews']
        tokenisasiteks = tokenisasi(text)
        tfidfteks = tfidffuc(tokenisasiteks) 
        dftfidftext = dftfidf(tokenisasiteks)
        similarity = cosine(tfidfteks) 
        similaritytoarray = similarity.toarray() 
        matrik_adjencey = res_graph_adjencey(similarity)
        skor_pagerank = pagerank(matrik_adjencey) 
        pengurutan_skor = sorted_sentences(skor_pagerank, tokenisasiteks)
        
        if not request.form['numOfLines']: 
            numOfLines = 5
        else:
            numOfLines = int(request.form['numOfLines']) 
        peringkasan = summarytopn(pengurutan_skor, numOfLines) 
        
        return render_template('success_artikel_non.html', output_text=text, 
                                                        tokenized=tokenisasiteks, 
                                                        tables=[dftfidftext.to_html(classes='table table-bordered',index=False)], 
                                                        titles=dftfidftext.columns.values, 
                                                        similarity_text=similaritytoarray, 
                                                        score_pagerank=skor_pagerank, 
                                                        sorted_score=pengurutan_skor,
                                                        summary=peringkasan
                                                        )



# Evaluasi hasil peringkasan 
@app.route('/convert_eval', methods=['POST', 'GET'])
def convert_eval(): # inisialisai functiom

    target = os.path.join(APP_ROOT)
    # print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    # looping untuk memeriksa rekues dari file 
    for file in request.files.getlist('file'):
        # kondisi dimana file ada
        if allowed_file(file.filename):
            # print(file)
            filename_text = file.filename
            destination = '/'.join([target, filename_text])
            # print(destination)
            file.save(destination) # save destination file
            filename = destination
            filenametext = converter(filename) #convert file pdf ke dalam bentuk teks

        else:
            return render_template('error.html') # kondisi dimana jika file salah atau kosong 


    # looping untuk memeriksa rekues dari file 
    for file in request.files.getlist('file2'):
        # kondisi dimana file ada
        if allowed_file(file.filename):
            # print(file)
            filename_text = file.filename
            destination = '/'.join([target, filename_text])
            # print(destination)
            file.save(destination) # save destination file
            filename = destination
            filenametext2 = converter(filename) #convert file pdf ke dalam bentuk teks

            hasil_evaluasi=evaluation_rouge(filenametext, filenametext2) # perhitungan score evaluasi Rouge

        else:
            return render_template('error.html') # ika file salah atau kososng

    # Render tempelt success evaluation jika kondisi semua terpenuhi dengan mengirimkan nilai ke halaman tersebut
    return render_template('success_evaluation.html', output_text=filenametext, output_ref=filenametext2, output_hasil=hasil_evaluasi)


# Unduh hasil peringkasan 
@app.route('/convert_download', methods=['POST', 'GET'])
def convert_download(): 
    if request.method == 'POST':
        text = request.form['ringkasan']

    return render_template('download.html', ringkasan=text)

# Unduh hasil peringkasan ke pdf
@app.route('/save_pdf', methods=['POST','GET'])
def save_pdf():
    if request.method == 'POST':
        text = request.form['ringkasan']

    html = render_template("download.html", ringkasan=text)

    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"

    return response


# run program
if __name__ == '__main__':
    app.run(debug = True)