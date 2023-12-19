# -*- coding: utf-8 -*-
"""local_website_documentation_summary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sMevU4v9FUJWSpDhosQ6ykUCjjlHP8tn
"""

!pip install langchain
!pip install huggingface_hub transformers datasets

import os

# 허깅페이스 LLM Read Key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "beomi/llama-2-ko-7b"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained('./llama-2-ko-7b')
tokenizer.save_pretrained('./llama-2-ko-7b')

from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain import LLMChain

from langchain.llms import HuggingFaceHub

# 네이버 뉴스기사 주소
url = 'https://n.news.naver.com/article/437/0000361628?cds=news_media_pc'

# 웹 문서 크롤링
loader = WebBaseLoader(url)

# 뉴스기사의 본문을 Chunk 단위로 쪼갬
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=3000,     # 쪼개는 글자수
    chunk_overlap=300,   # 오버랩 글자수
    length_function=len,
    is_separator_regex=False,
)

# 웹사이트 내용 크롤링 후 Chunk 단위로 분할
docs = WebBaseLoader(url).load_and_split(text_splitter)

# 각 Chunk 단위의 템플릿
template = '''다음의 내용을 한글로 요약해줘:

{text}
'''

# 전체 문서(혹은 전체 Chunk)에 대한 지시(instruct) 정의
combine_template = '''{text}

요약의 결과는 다음의 형식으로 작성해줘:
제목: 신문기사의 제목
주요내용: 한 줄로 요약된 내용
작성자: 김철수 대리
내용: 주요내용을 불렛포인트 형식으로 작성
'''

# 템플릿 생성
prompt = PromptTemplate(template=template, input_variables=['text'])
combine_prompt = PromptTemplate(template=combine_template, input_variables=['text'])

# 로컬 모델 및 토크나이저 로딩
model_path = './llama-2-ko-7b'  # 로컬 모델 경로
local_model = AutoModelForCausalLM.from_pretrained(model_path)
local_tokenizer = AutoTokenizer.from_pretrained(model_path)

#from langchain_core.runnables.llm import LLMRunnable

#llm_runnable = LLMRunnable(model=local_model, tokenizer=local_tokenizer)

#llm_chain = LLMChain(llm=llm_runnable, prompt=prompt)
from langchain.llms import HuggingFace
llm = HuggingFace(model_name=local_model, temperature=0.9)

# LLMChain 객체 생성, 로컬 모델 및 토크나이저 전달
llm_chain = LLMChain(llm = llm, tokenizer=local_tokenizer, prompt=prompt)

# 요약을 도와주는 load_summarize_chain
chain = load_summarize_chain(llm_chain,
                             map_prompt=prompt,
                             combine_prompt=combine_prompt,
                             chain_type="map_reduce",
                             verbose=False)

# 실행결과
print(chain.run(docs))

# HuggingFaceHub 대신 로컬 모델 및 토크나이저를 사용하여 LLMChain 객체 생성
llm_chain = LLMChain(llm=local_model, tokenizer=local_tokenizer, prompt=prompt)

# HuggingFaceHub 객체 생성
# llm = HuggingFaceHub(repo_id='beomi/llama-2-ko-7b', model_kwargs={"temperature": 0.1, "max_length": 128})

# 요약을 도와주는 load_summarize_chain
chain = load_summarize_chain(llm_chain,
                             map_prompt=prompt,
                             combine_prompt=combine_prompt,
                             chain_type="map_reduce",
                             verbose=False)

# 실행결과
print(chain.run(docs))