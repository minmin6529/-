# -*- coding: utf-8 -*-
"""Website-documentation-summary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jX3wByE6ok_iEhWnOcNMIezo6g22USFz
"""

!pip install langchain
!pip install huggingface_hub transformers datasets

import os

# 허깅페이스 LLM Read Key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

# 토큰 정보로드를 위한 라이브러리
! pip install python-dotenv
from dotenv import load_dotenv

# 토큰 정보로드
load_dotenv()

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


# 네이버 뉴스기사 주소
url = 'https://n.news.naver.com/mnews/article/025/0003311700?sid=101'

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
docs

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

# HuggingFace Repository ID
repo_id = 'beomi/llama-2-ko-7b'

# HuggingFaceHub 객체 생성
llm = HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature": 0.1,
                  "max_length": 128}
)

# 요약을 도와주는 load_summarize_chain
chain = load_summarize_chain(llm,
                             map_prompt=prompt,
                             combine_prompt=combine_prompt,
                             chain_type='map_reduce',
                             verbose=False)

# 실행결과
print(chain.run(docs))