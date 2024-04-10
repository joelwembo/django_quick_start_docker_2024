from django.http import JsonResponse


def list_pets(request):
    return JsonResponse(
        {
            "status": 200,
            "items": [
                {
                    "name": "Mac",
                    "species": "dog",
                    "age": 4,
                },
                {
                    "name": "Tom",
                    "species": "cat",
                    "age": 6,
                },
            ],
        }
    )
