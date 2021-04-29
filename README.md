# The implementation of HDSKG using BERT model
[Paper link](https://ieeexplore.ieee.org/abstract/document/7884609)
## The architecture of HDSKG is as follows:
<!-- ![HDSKG-Framework](res/img/HDSKG-Framework.jpg) -->
<div align="center">
      <img src="./res/img/HDSKG-Framework.jpg" width = "80%" alt="HDSKG-Framework" align=center />
</div>

## Installation
1. `pip install -r requirements.txt`
2. I use [stanza](https://github.com/stanfordnlp/stanza) to access __Stanford CoreNLP__, I suggest installing it from source of its git repository
   ```bash
   git clone https://github.com/Rvlis/stanza.git
   cd stanza
   pip install -e .
   ```
3. Manually download [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) or use __stanza.install_corenlp("your/absolute/path")__
4. Setting the `CORENLP_HOME` environment variable with the __your/absolute/path__
5. I use __Spacy__ and __[neuralcoref](https://github.com/huggingface/neuralcoref)__ to resolve coreference, install neuralcoref from source as well
   ```bash
   git clone https://github.com/Rvlis/neuralcoref.git
   cd neuralcoref
   pip install -r requirements.txt
   pip install -e .
   ```
6. Don't forget loading spacy's model, which is dependent on your spacy's version. Here `2.3.*` is ok.

## Usage
1. [HDSKG-Chunking](./HDSKG-Chunking/)
2. [HDSKG-Domain-Relevance-Estimation](./HDSKG-Domain-Relevance-Estimation/)
3. [Generate-Domain-Knowledge-Graph](./Generate-Domain-Knowledge-Graph/)


## Test Bert Model
Compared with previous __0.76__, accuracy is improved to __0.82__ now.
The `checkpoint` file will be uploaded soon.
__TODO__

## Knowledge Graph
![KG](res/img/KG-neo4j.jpg)

## TODO
package all parts









