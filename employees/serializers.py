from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "email", "department", "role", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def validate_name(self, value: str) -> str:
        if value is None or not str(value).strip():
            raise serializers.ValidationError("Name must not be empty.")
        return value.strip()
