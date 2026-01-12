# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Recipes(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    difficulty = models.IntegerField()
    image = models.BinaryField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    preparation = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipes'

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField()
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'users'

class UserSession(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    session_token = models.CharField(unique=True, max_length=100)

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    active = models.BooleanField(default=False)
    image = models.BinaryField(blank=True, null=True)

class CategoryRecipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

class UserFavoriteRecipe(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

