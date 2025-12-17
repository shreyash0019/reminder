@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_device(request):
    Device.objects.update_or_create(
        fcm_token=request.data["fcm_token"],
        defaults={"user": request.user}
    )
    return Response({"status": "ok"})
