from ninja import Router

router = Router()

@router.get('/hello')
def hello(request):
    return "Hello world"


@router.get('/hello22')
def hello(request):
    return "Hello world"