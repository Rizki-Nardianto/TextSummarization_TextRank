# request 
import requests

# import modul
from io import StringIO

# import os
import os

# untuk app flask, file, bootstrap
from flask import Flask, render_template, request, flash, send_file, Response, make_response

# modul regek
import re

# request 
import requests

# mdoul perhitungan matematika 
import numpy as np

# modul pandas
import pandas as pd

import scipy as sp
import scipy.sparse  # call as sp.sparse

# parsing artikel
from bs4 import BeautifulSoup

# untuk perhitungan pagerank
import networkx as nx

# untuk evaluasi peringkasan
from rouge import Rouge

# untuk tokenisasi kalimat dan kata
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Filtering Module (Sastrawi)
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

#Pandas and Matplotlib
import pandas as pd 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# untuk perhitungan bobot tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# html to pdf
import pdfkit

# untuk menginterpretasi halaman pdf
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

#untuk mengubah file pdf ke text
from pdfminer.converter import TextConverter

#untuk menampilkan pdf
from pdfminer.layout import LAParams

# untuk menghitung halaman pdf
from pdfminer.pdfpage import PDFPage