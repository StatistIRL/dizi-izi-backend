from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db import transaction
from furniture.models import (
    Furniture,
    Room,
    Placement,
    PowerSocket,
    Door,
    Window,
    Coordinate
)
from . import algorithm

FIELDS_COORDINATE = (
            'north_west',
            'north_east',
            'south_west',
            'south_east',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'password')


class FurnitureSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    class Meta:
        fields = (
            'id',
            'name',
            'name_english',
            'length',
            'width',
            'length_access',
            'width_access',
        )
        model = Furniture


class CoordinateSerializer(serializers.ModelSerializer):
    """Сериализатор для координат x,y."""

    class Meta:
        fields = (
            'x',
            'y'
        )
        model = Coordinate


class AbstractCoordinates(serializers.Serializer):
    """Абстрактная модель для координат в сериализаторах."""
    north_west = CoordinateSerializer()
    north_east = CoordinateSerializer()
    south_west = CoordinateSerializer()
    south_east = CoordinateSerializer()

    class Meta:
        abstract = True


class PlacementSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения мебели в комнате."""

    class Meta:
        fields = ('furniture',) + FIELDS_COORDINATE
        model = Placement


class PowerSocketSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = FIELDS_COORDINATE
        model = PowerSocket


class DoorSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = (
            'width',
            'open_inside',) + FIELDS_COORDINATE
        model = Door


class WindowSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения окон в помещении."""

    class Meta:
        fields = (
            'length',
            'width',) + FIELDS_COORDINATE
        model = Window


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""
    furniture_placement = PlacementSerializer(
        many=True,
        source='placements'
    )
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True
    )
    power_sockets = PowerSocketSerializer(
        many=True,
        read_only=True,
        source='powersockets'
    )
    doors = DoorSerializer(
        many=True,
    )
    windows = WindowSerializer(
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'first_wall',
            'second_wall',
            'third_wall',
            'fourth_wall',
            'furniture_placement',
            'selected_furniture',
            'doors',
            'power_sockets',
            'windows'
        )
        model = Room
        read_only = ('id', )

    @transaction.atomic
    def create(self, validated_data):
        """Создание помещения с расстановкой."""

        def create_get_coordinate_item(placement):
            """Создать и вернуть координаты для элемента (мебель, окно,...)"""
            return {
                'north_west': Coordinate.objects.create(
                    x=placement['north_west']['x'],
                    y=placement['north_west']['y']
                ),
                'north_east': Coordinate.objects.create(
                    x=placement['north_east']['x'],
                    y=placement['north_east']['y']
                ),
                'south_west': Coordinate.objects.create(
                    x=placement['south_west']['x'],
                    y=placement['south_west']['y']
                ),
                'south_east': Coordinate.objects.create(
                    x=placement['south_east']['x'],
                    y=placement['south_east']['y']
                ),
            }

        room_placement = validated_data.pop('placements')
        selected_furniture = validated_data.pop('selected_furniture')
        doors = validated_data.pop('doors')
        windows = validated_data.pop('windows')
        room = Room.objects.create(**validated_data)
        furniture_placement = []
        for placement in room_placement:
            furniture = placement['furniture']
            coordinates = create_get_coordinate_item(placement)
            furniture_placement.append(
                Placement(
                    furniture=furniture,
                    room=room,
                    **coordinates
                )
            )
        Placement.objects.bulk_create(furniture_placement)
        room_doors = []
        for door in doors:
            coordinates = create_get_coordinate_item(door)
            room_doors.append(
                Door(
                    width=door['width'],
                    open_inside=door['open_inside'],
                    room=room,
                    **coordinates
                )
            )
        Door.objects.bulk_create(room_doors)
        room_windows = []
        for window in windows:
            coordinates = create_get_coordinate_item(window)
            room_windows.append(
                Window(
                    width=window['width'],
                    length=window['length'],
                    room=room,
                    **coordinates
                )
            )
        Window.objects.bulk_create(room_windows)
        furniture_placement = []
        for furniture in selected_furniture:
            # здесь применение алгоритма по расстановке мебели
            pass
        return room

    def save(self, **kwargs):
        if not kwargs['user']:
            room = self.validated_data
            selected_furniture = room.pop('selected_furniture')
            fp = algorithm.FurnitureArrangement()
            doors_and_windows = room['doors']
            furniture = []
            room_size = {
                'first_wall': room['first_wall'],
                'second_wall': room['second_wall'],
                'third_wall': room['third_wall'],
                'fourth_wall': room['fourth_wall'],
            }
            fp.algorithm_activation(
                doors_and_windows, furniture, room_size
            )
            print(fp)
            for furniture in selected_furniture:
                pass
            #     # здесь применение алгоритма по расстановке мебели
            #     one_furniture_placement = {}
            #     one_furniture_placement['furniture']=furniture
            #     one_furniture_placement['nw_coordinate']=12
            #     one_furniture_placement['ne_coordinate']=13
            #     one_furniture_placement['sw_coordinate']=14
            #     one_furniture_placement['se_coordinate']=15
            #     room['placements'].append(one_furniture_placement)
            self.instance = room
        else:
            self.instance = super().save(**kwargs)
        return self.instance
