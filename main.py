import http
from starlette.requests import ClientDisconnect, Request, State
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.responses import JSONResponse
import os
import shutil


async def get_images(request):
    currentDirectory = os.getcwd()
    dataset_directory_path = currentDirectory + '/data/eloc_dataset'
    files = os.listdir(dataset_directory_path)
    req = request.path_params['q']
    print(req)
    initial = 0
    steps = 50
    if req == 1:
        first = 0
        end = 50
    else:
        end = initial + int(req) * steps
        first = end - steps
        print((first + 1, end))
    return JSONResponse(files[first:end])


async def bad_images(request):

    data = await request.json()
    bad_image = data['bad_image']
    for fileName in os.listdir(os.getcwd() + '/data/eloc_dataset'):
        if fileName == bad_image:

            shutil.copy(os.getcwd() + '/data/eloc_dataset/' + fileName, os.getcwd() + '/data/bad')

    return JSONResponse({'status': 'ok'})


routes = [
    Route("/images/{q}", endpoint=get_images, methods=['GET', 'POST']),
    Route('/bad-image', endpoint=bad_images, methods=['POST'])
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run('main:app')
