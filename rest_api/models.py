# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField()
    image = models.BinaryField(blank=True, null=True)
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'category'


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField()
    description = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.IntegerField()
    image = models.BinaryField(blank=True, null=True)
    ingredients = models.CharField(max_length=1000, blank=True, null=True)
    preparation = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=50)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'recipe'


class RecipeCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_categories'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField()
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'user'


class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=36)
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'session'


class UserFavoriteRecipes(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_favorite_recipes'
