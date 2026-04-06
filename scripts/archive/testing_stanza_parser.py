import stanza

nlp = stanza.Pipeline(
    lang='is',
    processors='tokenize, pos, constituency',
    constituency_model_path='/Users/esther/Documents/GitHub/stylometry-icelandiceval/models/is_icepahc_transformer_finetuned_constituency.pt'
)
headlines = [
    "Eg mun hér vera að eigi komist maðurinn út ef hann er hér inni en þú GAKK til stofu",
    "'Gerðu annaðhvort,' sagði húskarl, 'að þú FAR á brott eða gakk inn og ver hér í nótt'" 
]

for h in headlines:
    doc = nlp(h)
    tree = str(doc.sentences[0].constituency)
    has_subject = 'NP*SBJ' in tree
    print(f"{'✓' if has_subject else '✗'} {h}")

doc = nlp("Eg mun hér vera að eigi komist maðurinn út ef hann er hér inni en þú GAKK til stofu")
print(str(doc.sentences[0].constituency))
for sentence in doc.sentences:
    tree = str(sentence.constituency).replace('*', '-')
    tree = tree.replace('ROOT ', '')
    print(tree)

doc = nlp("'Gerðu annaðhvort,' sagði húskarl, 'að þú FAR á brott eða gakk inn og ver hér í nótt'")
print(str(doc.sentences[0].constituency))
for sentence in doc.sentences:
    tree = str(sentence.constituency).replace('*', '-')
    tree = tree.replace('ROOT ', '')
    print(tree)

doc = nlp('þú FAR á brott og gakk inn og ver hér í nótt')
print(str(doc.sentences[0].constituency))
for sentence in doc.sentences:
    tree = str(sentence.constituency).replace('*', '-')
    tree = tree.replace('ROOT ', '')
    print(tree)