import stanza

nlp = stanza.Pipeline(
    lang='is',
    processors='tokenize, pos, constituency',
    constituency_model_path='/Users/esther/Documents/GitHub/stylometry-icelandiceval/models/is_icepahc_transformer_finetuned_constituency.pt'
)
headlines = [
    "KPMG opnar skrifstofu á Blönduósi",
    "Viltu taka þátt í vöruþróun ?",
    "Íbúum Blönduóss og Skagastrandar fjölgar",
]

for h in headlines:
    doc = nlp(h)
    tree = str(doc.sentences[0].constituency)
    has_subject = 'NP*SBJ' in tree
    print(f"{'✓' if has_subject else '✗'} {h}")

doc = nlp('Íbúum Blönduóss og Skagastrandar fjölgar')
print(str(doc.sentences[0].constituency))
for sentence in doc.sentences:
    tree = str(sentence.constituency).replace('*', '-')
    tree = tree.replace('ROOT ', '')
    print(tree)

doc = nlp('Viltu taka þátt í vöruþróun ?')
print(str(doc.sentences[0].constituency))
for sentence in doc.sentences:
    tree = str(sentence.constituency).replace('*', '-')
    tree = tree.replace('ROOT ', '')
    print(tree)

doc = nlp('KPMG opnar skrifstofu á Blönduósi')
print(str(doc.sentences[0].constituency))
for sentence in doc.sentences:
    tree = str(sentence.constituency).replace('*', '-')
    tree = tree.replace('ROOT ', '')
    print(tree)