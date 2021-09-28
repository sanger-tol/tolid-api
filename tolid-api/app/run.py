from main import application

app = application()
reload = True


def main():
    print("Starting ToLID application...")
    app.run(host='0.0.0.0', debug=True, port=80, use_reloader=reload)


if __name__ == '__main__':
    main()
