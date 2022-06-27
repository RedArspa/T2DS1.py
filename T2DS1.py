import csv
import streamlit as st
import datasketch as ds


def create_shinglebag(k=3):
    """ Creates a bag of k-shingles from the Dataset. Replaces ";:,. from the strings."""
    file = open('mtsamples.csv', encoding='utf-8')
    csvreader = csv.reader(file)
    header, rows, shinglebag, shingles, k_shingle = [], [], [], [], ""
    header = next(csvreader)
    i = 0
    for row in csvreader:
        rows.append(row[4].replace(",", "").replace(":", "").replace(".", "").replace(";", "").lower().split())
        i += 1
        if i > 1000:
            break
    for row in rows:
        for word in range(len(rows)):
            try:
                for i in range(k):
                    k_shingle += str(row[word + i]) + " "
            except:
                pass
            shingles.append(k_shingle.strip())
            if k_shingle == "":
                break
            k_shingle = ""
        shinglebag.append(shingles)
        shingles = []
    return shinglebag


def minhash(bag_one, bag_two, hashcount=100):
    """Minhash two bags of words with a number of hash functions and returns the jaccard similarity"""
    hash_one = ds.MinHash(num_perm=hashcount)
    hash_two = ds.MinHash(num_perm=hashcount)
    for i in bag_one:
        hash_one.update(i.encode("utf8"))
    for i in bag_two:
        hash_two.update(i.encode("utf8"))
    print(hash_one.jaccard(hash_two))
    return hash_one.jaccard(hash_two)


st.write("### Word Level Shiinging Similarty")
hashcount = st.slider('Number of hashfunctions', value=100, min_value=1, max_value=1000)
shinglesize = st.slider('Shingle size', value=5, min_value=1, max_value=15)
shinglebag = create_shinglebag(shinglesize)
doc1 = st.selectbox("Select bag 1:", shinglebag, index=0)
doc2 = st.selectbox("Select bag 2:", shinglebag, index=0)

st.write("###### The estimated Jaccard similarity is:",
         minhash(shinglebag[shinglebag.index(doc1)], shinglebag[shinglebag.index(doc2)], hashcount))
st.write("###### The real Jaccard similarity is:     ", (float(
    len(set(shinglebag[shinglebag.index(doc1)]).intersection(set(shinglebag[shinglebag.index(doc2)])))) / float(
    len(set(shinglebag[shinglebag.index(doc1)]).union(set(shinglebag[shinglebag.index(doc2)]))))))
