# Exploring the Transferability of Domain Specific Models for NER on Historic Datasets

>[!NOTE]
>This is a student project and my first attempt at working with transformers or preprocessing data for NER.
>All files in this repository should be treated as experimental and I am sure anyone with more experience with NLP will be acutely aware of the shortcomings of these attempts or the idiosyncrasies of the code.

## Libraries and Dependencies
The notebooks were run on Google Colab. The fine tuning was done on a GPU-Accelerated runtime (V-100 GPU and high RAM).
The NLP libraries required to run these notebooks are (version used in parentheses):
- SpaCy (3.7.4)
- Huggingface Transformers (4.38.2)
- Flair (0.13.1)
- Sklearn (1.2.2)
- Pytorch (2.2.1+cu121)

## Aim and Scope
This project aims at comparing the performance of a selection of language models for the purpose of _named entity recognition_ in historical corpora. 
In particular, it compares two transformer models and models from SpaCy both 'as is' and fine-tuned on the domain specific data.
It furthermore asks the question whether it would be more worthwhile to fine-tune a generic language model, or one that was pre-trained on historical data, given that the application
domain is neither modern language, nor exactly the kind of historical language a historical language model would be pre-trained on.
These tests are exploratory in nature and were conceived with the scenario of student projects or comparable situations with very limited time and resources in mind.
The tests comprise evaluations of six models (3 'as is' and 3 fine-tuned), the training of the best performing model on smaller and denser datasets, and a set of adversarial tests.
The models are: de_core_news_sm (used as is), a custom trained SpaCy NER pipeline, ner-bert-german (used as is), bert-base-german-cased (fine-tuned), flair-historic-ner-onb (used as is), and flair-historic-ner-onb (fine-tuned).

This repository contains the data files, tables with comparisons of the model performances, and the jupyter notebooks used to preprocess the data, 
create the default / smaller / denser / adversarial datasets, as well as to fine-tune, run, and evaluate the various models.

## Datasets
The application domain of these tests is highly specific: The corpus is comprised of German religious texts of the 17th and 18th century.
They are sourced from the DFG-Project [Deutsche Orgelpredigtdrucke zwischen 1600 und 1800 – Katalogisierung, Texterfassung, Auswertung](https://orgelpredigt.ur.de/) and the [Austrian Baroque Corpus (ABaC:us)](https://acdh.oeaw.ac.at/abacus/).
The data comprises a total of **798,912 tokens, or 30,873 sentences**. The corpus is released here as part of the project in a somewhat spartanic implementation of the CONLL format 
under a Creative Commons 4.0 BY-NC-SA license and can be found at the location [data/train_test_val](data/train_test_val), which contains both the complete dataset and train and test files generated from it for this project.

## Repository Structure
The general approach of this repository was to keep each task as self contained as possible.
Each task therefore is contained in an independent notebook and writes its results to .tsv or .csv files.
Not included here are the models due to their number and size. They are available upon request.

- The root directory of this repository contains the jupyter notebooks for preprocessing the data, for running both models relying both on the Flair and Huggingface Transformer libraries, as well as for evaluating and visualising the results. Additionally, the files [bible_abbr] and [latin_abbr] contain lists of frequent abbreviations that are used to resolve issues during preprocessing.
- The data directory contains preprocessed text files of the individual source documents, the training/testing data, the smaller training data, and the adversarial testing data
- The smaller_datasets directory contains the notebooks to create the datasets, fine-tune, run, and evaluate the models with that data
- The adversarial_data directory contains the same notebooks for the adversarial tests
- The model_comparisons directory contains the table with all predictions ([model_comparisons/test-predictions_comparison.tsv]) of the various models, as well as csv files that contain the evaluations of these predictions, both for all models and for the smaller models / adversarial tests in particular.
- The advers_model_comparisons directory contains the prediction tables for the seven adversarial tests.

## Results
>[!NOTE]
>As I explain in more detail in my project report, the results presented here are impacted by a number of limitations.
>In particular, due to the constraints of this course project, I could not perform extensive hyper parameter tweaking.
>I am certain that better performances with all models used here are possible.
>However, part of the project design was to simulate a situation of limited time and resources and in this case using parameters that don't stray too far from the defaults and don't use too many resources seemed appropriate.

The results seem to suggest that while all models benefit greatly from fine-tuning, the generic transformer model has the edge over both the historic transformer and the SpaCy model.

| Model | F1-Score | Precision | Recall |
|-------|----------|-----------|--------|
|bert-base-german-cased (f-t) | **0.6862** | 0.7891 | **0.6070** |
|flair-historic-ner-onb (f-t) | 0.5947 | **0.8024** | 0.4724 |
| Custom SpaCy | 0.5465 | 0.7078 | 0.4451 |
| ner-bert-german | 0.3743 | 0.3297 | 0.4328  |
| flair-historic-ner-onb | 0.3565 | 0.2996  | 0.4402 |
| de_core_news_sm | 0.2200 | 0.1431 | 0.4751 |

The tests of the smaller and denser datasets suggest a medium hit to performance for half the training data and from there a steady decline upon further reduction.
The tests with denser datasets (only sentences with NEs (F1: 0.5482 )/ all sentences with NEs + 10% sentences without (F1: 0.5731)) suggest that a small percentage of non-NE sentences helps prevent excessive false positives.
The mean results of the seven adversarial tests confirm the robustness of the generic language model which comes up on top, with the fine-tuned historic model taking the greatest hit.

## Thanks, Links, and References
This project would not have been possible were it not for the following great resources:

- The ABaC:us Project: *ABaC:us – Austrian Baroque Corpus*. Ed. by Claudia Resch and Ulrike Czeitschner. 2015. url: http://acdh.oeaw.ac.at/abacus/ (visited on 03/28/2024).
- The DFG Project Deutsche Orgelpredigtdrucke: *DFG-Projekt „Deutsche Orgelpredigtdrucke Zwischen 1600 Und 1800 – Katalogisierung, Texterfassung, Auswertung“*. Ed. by Katelijne Schiltz, Lucinde Braun et. al. 2023. url: https://orgelpredigt.ur.de (visited on 03/28/2024).
- The [bert-base-german-cased model](https://huggingface.co/dbmdz/bert-base-german-cased) and the [flair-historic-ner-onb model](https://huggingface.co/dbmdz/flair-historic-ner-onb) provided on the Huggingface Hub by the dbmdz team
- The [ner-bert-german model](https://huggingface.co/mschiesser/ner-bert-german) provided on the Huggingface Hub by Marcus Schiesser.
- The [Token Classification Course](https://huggingface.co/learn/nlp-course/en/chapter7/2) on Huggingface
- The [Flair Documentation](https://flairnlp.github.io/docs/intro), especially the chapters on datasets and sequence tagging
- The YouTube series [*Named Entity Recognition in Python for Digital Humanities*](https://www.youtube.com/watch?v=2Ny0yATnuxY)
- The SpaCy, HuggingFace Transformers, and Flair libraries
- The team behind the NLP course at Regensburg University who kindly helped me with the various issues I encountered along the way

