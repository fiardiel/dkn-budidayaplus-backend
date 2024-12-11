from django.test import TestCase
from user_profile.schemas import CreateWorkerSchema
from pydantic import ValidationError

class CreateWorkerSchemaTest(TestCase):
    def test_validate_password(self):
        schema = CreateWorkerSchema(
            phone_number='081234567890',
            first_name='Rafi',
            last_name='Ardiel',
            password='abc1234hijk'
        )
        self.assertEqual(schema.password, 'abc1234hijk')

    def test_validate_password_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            CreateWorkerSchema(
                phone_number='081234567890',
                first_name='Rafi',
                last_name='Ardiel',
                password='abc123'
            )

        self.assertIn('Password harus minimal 8 karakter', str(context.exception))

    def test_validate_password_no_digit(self):
        with self.assertRaises(ValidationError) as context:
            CreateWorkerSchema(
                phone_number='081234567890',
                first_name='Rafi',
                last_name='Ardiel',
                password='abcdefgh'
            )

        self.assertIn('Password harus mengandung angka', str(context.exception))

    def test_validate_password_no_alphabet(self):
        with self.assertRaises(ValidationError) as context:
            CreateWorkerSchema(
                phone_number='081234567890',
                first_name='Rafi',
                last_name='Ardiel',
                password='12345678'
            )

        self.assertIn('Password harus mengandung huruf', str(context.exception))


    def test_validate_password_minimum_length(self):
        schema = CreateWorkerSchema(
            phone_number='081234567890',
            first_name='Rafi',
            last_name='Ardiel',
            password='abcd1234'
        )
        self.assertEqual(schema.password, 'abcd1234')

    def test_validate_password_only_one_digit(self):
        schema = CreateWorkerSchema(
            phone_number='081234567890',
            first_name='Rafi',
            last_name='Ardiel',
            password='abcdefg1'
        )
        self.assertEqual(schema.password, 'abcdefg1')

    def test_validate_password_only_one_alphabet(self):
        schema = CreateWorkerSchema(
            phone_number='081234567890',
            first_name='Rafi',
            last_name='Ardiel',
            password='1234567a'
        )
        self.assertEqual(schema.password, '1234567a')

