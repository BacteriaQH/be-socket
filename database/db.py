from database.models import Users, Units, Files, Approves


def add_user(data):
    user = Users(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        age=data['age'],
        address=data['address'],
    )
    user.save()
    print('saved user')


def add_unit(data):
    try:
        unit = Units(
            name=data['name'],
            mst=data['MST'],
            address=data['address'],
            user=data['user'],
            admin=data['admin'],
            socket_id=data['socket_id'],
            adminName=data['adminName'],
            room_name=data['room_name'],
        )
        unit.save()
        print('saved unit')
    except Exception as e:
        print('false from add unit')
        print(e)


def add_file(data):
    file = Files(
        code=data['code'],
        name=data['name'],
        link=data['link'],
        createFileBy=data['createFileBy'],
    )
    file.save()
    print('saved file')


def find_user(email, password):
    user = Users.objects.get(email=email)
    return user


def get_files():
    files = Files.objects()
    return files


def update_file(id, isSign, signFileBy, link, time_sign):
    file = Files.objects(id=id).update(set__isSign=isSign, set__signFileBy=signFileBy, set__link=link, set__signFileAt=time_sign)
    return True


def get_file_id(data):
    file = Files.objects.get(id=data)
    return file
# def add_user_to_unit(data):
#     pass
#
#
# def add_file(data):
#     pass
