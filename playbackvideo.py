import os
from fastapi import FastAPI, HTTPException, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from dotenv import load_dotenv
from supabase import create_client, Client
import httpx
from datetime import datetime,timezone
UTC=timezone.utc
import subprocess

load_dotenv()

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

templates = Jinja2Templates(directory="templates")

templates.env.globals.update(now=lambda:datetime.now(UTC))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_BUCKET= os.getenv('SUPABASE_BUCKET')

supabase: Client = create_client(SUPABASE_URL,SUPABASE_ANON_KEY)

@app.get('/',response_class= HTMLResponse)
async def homepage(request:Request):
  return templates.TemplateResponse('responsive.html',{"request":request})

@app.get('/{filename}',response_class=HTMLResponse)
async def home(filename:str):
  try:
   video_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
  except Exception as e:
   raise HTTPException(status_code=500,detail=" failed to fetch video list ")
  async def video_stream():
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url, follow_redirects=True)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch video")
            
            async for chunk in response.aiter_bytes(chunk_size=8192):
                yield chunk

  return StreamingResponse(video_stream(), media_type='video/mp4')
  
 
  # videos = supabase.storage.from_(SUPABASE_BUCKET).list()
  # return templates.TemplateResponse('home.html',{'request':request,'videos':videos})

@app.get('/videos/{video_name}')
async def get_video(video_name:str):
  video_url=supabase.storage.from_(SUPABASE_BUCKET).get_public_url(video_name)
  
  if not video_url:
    return {'error':'video not found'}
  
  async def video_stream():
    async with httpx.AsyncClient() as client:
      response = await client.get(video_url,headers={'Range':'bytes=0-'},timeout=None,follow_redirects=True)
      if response.status_code not in [200, 206]:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch video")
      async for chunk in response.aiter_bytes(chunk_size=8192):
        yield chunk    
          
  return StreamingResponse(video_stream(),media_type='video/mp4')

@app.get('/live')
async def GOlive():
# Convert MP4 to AVI
 subprocess.run(['ffmpeg', '-i', 'input.mp4', 'output.m3u8'])