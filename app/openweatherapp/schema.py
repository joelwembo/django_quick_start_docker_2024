import graphene
from graphene_django import DjangoObjectType
from .models import City

  
class CityType(DjangoObjectType):
    class Meta:
        model = City
        fields = ("id", "name")    
                

class Query(graphene.ObjectType):
  """
  Queries for the City model
  """
  Cities = graphene.List(CityType)

  def resolve_Cities(self, info, **kwargs):
    return City.objects.all()


class CreateCity(graphene.Mutation):
  class Arguments:
    name = graphene.String()

  ok = graphene.Boolean() 
  City = graphene.Field(CityType)

  def mutate(self, name):
    City = City(name=name)
    City.save()
    return CreateCity(ok=True, City=City)

class DeleteCity(graphene.Mutation):
  class Arguments:
    id = graphene.Int()

  ok = graphene.Boolean()

  def mutate(self, info, id):
    City = City.objects.get(id=id)
    City.delete()
    return DeleteCity(ok=True)


class UpdateCity(graphene.Mutation):
  class Arguments:
    id = graphene.Int()
    name = graphene.String()
   

  ok = graphene.Boolean()
  City = graphene.Field(CityType)

  def mutate(self, info, id, name):
    City = City.objects.get(id=id)
    City.name = name

    City.save()
    return UpdateCity(ok=True, City=City)


class Mutation(graphene.ObjectType):
  create_City = CreateCity.Field()
  delete_City = DeleteCity.Field()
  update_City = UpdateCity.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)