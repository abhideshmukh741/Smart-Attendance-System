from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import streamlit as st
import io
import librosa
from src.database.db import get_all_students

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_file):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_file.read()), sr=16000)
        wav= preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None
    

def identify_speaker(new_embedding,candidates_dir,threshold=0.65):
    if new_embedding is None or not candidates_dir:
        return None,0.0
    best_sid=None
    best_score=-1.0
    for sid,stored_embedding in candidates_dir.items():
        if stored_embedding:
            simmilarity=np.dot(new_embedding,stored_embedding)
            if simmilarity>best_score:
                best_score=simmilarity
                best_sid=sid
    if best_score>=threshold:
        return best_sid,best_score
    return None,best_score

def process_bulk_attendance(audio_file,candidates_dir,threshold=0.65):
    try:
        encoder=load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_file), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        identify_results={}
        for start,end in segments:
            if (end-start)<sr*0.5:
                continue  
            segment_audio=audio[start:end]
            wav=preprocess_wav(segment_audio)
            embedding=encoder.embed_utterance(wav)
            sid,score=identify_speaker(embedding,candidates_dir,threshold)
            if sid:
                if sid not in identify_results or score>identify_results[sid]:
                    
                    identify_results[sid]=score
        return identify_results
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return {}
    
    