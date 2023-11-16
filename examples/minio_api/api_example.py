import io

import minio


def main():
    # создаем клиент
    # параметры подключения генерируются в веб интерфейсе хранилища на порту 9090, когда будет сервак они меняться не будут
    client = minio.Minio(
        "localhost:9000",
        "STS9GtnODgKPvimPR5pm",
        "3pOTPpbOlw1MbBWHGG7k48ihidhehAiVg4zXC8J9",
        secure=False  # у нас нет ssl поэтому используем так
    )

    if not client.bucket_exists("zips"):
        client.make_bucket("zips")  # создаю бакет чтобы было куда складывать

    # основные действия которые нам понадобятся
    data = b"hello world"

    # положить объект в корзину
    client.put_object(
        "zips",  # bucket_name - по сути имя "папки" куда будет положен файл
        "task-id",  # object_name - имя файла в хранилище. нам, скорее всего, будет удобнее всего использовать
        io.BytesIO(  # идентификатор "таска" для имени файла
            data  # бинарные данные библиотека просит обернуть в io.BytesIO
        ),
        len(data)
    )

    # достать объект из корзины
    response = client.get_object(
        # библиотека под капотом по большей части реализует обертку над http api, потому здесь возвращается просто Response
        "zips",
        "task-id",
    )

    assert response.data == data  # сам файл лежит в поле response.data

    #удалить объект
    client.remove_object("zips", "task-id")

    try:
        response = client.get_object("zips", "task-id")
    except minio.error.S3Error:
        print("а файл то мы удалили, его больше не получить :)")


    print("вот и всё")


main()
