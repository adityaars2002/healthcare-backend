from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import DoctorSerializer, MappingSerializer, PatientSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {**serializer.data, "refresh": str(refresh), "access": str(refresh.access_token)},
            status=201,
        )


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class MappingViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MappingSerializer

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)

    def retrieve(self, request, pk=None):
        """GET /api/mappings/<patient_id>/ - the spec keys this route on patient id, not mapping id."""
        page = self.paginate_queryset(self.get_queryset().filter(patient_id=pk))
        return self.get_paginated_response(self.get_serializer(page, many=True).data)
