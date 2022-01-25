from dashboards import create_app
import sys
import os


__DEBUG__ = True if len(sys.argv) > 1 else False

app = create_app(__DEBUG__)

if __name__ == "__main__":
    if not __DEBUG__:
        os.startfile("http://localhost:5000")
    app.run(debug=__DEBUG__)
