import requests
import urllib.parse
from json import dumps, loads


class Tools:
    def __init__(self):
        pass

    def query_user(self, user: str) -> dict:
        """
        Obtain JSON-formatted information about a user of the website scratch.mit.edu. The user ID is not useful for anything and cannot be used in place of a username.

        :param user: A Scratch username as a string.
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/users/" + urllib.parse.quote_plus(user)
            ).text
        )

        del a["profile"]["images"]
        return a

    def query_messages(self, user: str) -> dict:
        """
        Obtain the number of unread notifications that a scratch.mit.edu user currently has. This is NOT related to project count.

        :param user: A Scratch username as a string.
        """

        return loads(
            requests.get(
                "https://api.scratch.mit.edu/users/"
                + urllib.parse.quote_plus(user)
                + "/messages/count"
            ).text
        )["count"]

    def query_projects(self, user: str, limit: int = 5, offset: int = 0) -> dict:
        """
        Obtain information about a scratch.mit.edu user's projects. Returns up to 40 projects per request, from the specified offset. Do not just put example strings in the parameters (that will not work and you will get unusable output).
        If the user is asking about someone's projects, they probably want detailed info of each project and not boilerplate templates for how it could be structured.
        Disregard any duplicate entries.

        This is NOT neccessarily the full list of the user's projects; increase the offset by the limit to see the next page of projects.

        :param user: A Scratch username as a string. Usernames are NOT the same as user IDs; user IDs are numbers whereas usernames are human-readable strings. Usernames should NOT be prefixed with the @ symbol.
        :param limit: The max number of projects to be fetched as an integer. Numbers over 40 will not yield usable results; use offsets instead. Optional and defaults to 5. If you need x amount of projects for some task where x<=40, set limit to x.
        :param offset: A numerical offset (integer) (see above documentation). This argument is optional.
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/users/"
                + urllib.parse.quote_plus(user.replace("@", ""))
                + "/projects/?limit=40&offset="
                + str(offset)
            ).text
        )

        for i in a:
            del i["author"]
            del i["image"]
            del i["images"]
        if a == "project_token":
            return {
                "error": "Project ID invalid. This is most likely because you made an ID up, unless the user specified an ID manually."
            }
        return a

    def query_id(self, id):
        """
        Obtain detailed information about a Scratch project given its ID. The ID is a number, usually provided by the user.

        :param id: A Scratch project ID as an integer
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/projects/"
                + urllib.parse.quote_plus(str(id))
                + "/"
            ).text
        )
        del a["author"]["profile"]
        del a["visibility"]
        del a["is_published"]
        del a["images"]
        del a["image"]
        del a["project_token"]
        return a

    def search_projects(self, query, limit=10):
        """
        Obtain JSON-formatted search results for Scratch projects matching a given query. Returns up to 40 projects per request.

        :param query: A search term as a string.
        :param limit: The max number of projects to be fetched as an integer, optional. Numbers over 40 will not yield usable results; the default is 10.
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/search/projects?q="
                + urllib.parse.quote_plus(query)
            ).text
        )

        for i in a:
            del i["author"]
            del i["image"]
            del i["images"]
        return dumps(a)

    def query_notes_from_id(self, id):
        """
        Obtain plaintext project Notes & Credits given an ID.

        :param id: A Scratch project ID as an integer
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/projects/"
                + urllib.parse.quote_plus(str(id))
                + "/"
            ).text
        )

        return a["description"]

    def query_instructions_from_id(self, id):
        """
        Obtain plaintext project Instructions given an ID.

        :param id: A Scratch project ID as an integer
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/projects/"
                + urllib.parse.quote_plus(str(id))
                + "/"
            ).text
        )

        return a["instructions"]

    def query_favorites(self, user, limit=5, offset=0):
        """
        Obtain JSON-formatted information about a scratch.mit.edu user's favorite projects. Returns up to 40 projects per request, from the specified offset.
        Disregard any duplicate entries.

        This is NOT neccessarily the full list of the user's projects; increase the offset by the limit to see the next page of projects.

        :param user: A Scratch username as a string. Usernames are NOT the same as user IDs; user IDs are numbers whereas usernames are human-readable strings. Usernames should NOT be prefixed with the @ symbol.
        :param limit: The max number of projects to be fetched as an integer. Numbers over 40 will not yield usable results; use offsets instead. Optional and defaults to 5. If you need x amount of projects for some task where x<=40, set limit to x.
        :param offset: A numerical offset (integer) (see above documentation). This argument is optional.
        """
        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/users/"
                + urllib.parse.quote_plus(user.replace("@", ""))
                + "/favorites/?limit=40&offset="
                + str(offset)
            ).text
        )

        for i in a:
            del i["author"]
            del i["image"]
            del i["images"]
        return dumps(a)

    def query_project_json(self, id: int) -> str:
        """
        Obtain JSON-formatted project code and data. Very large; do not reference unless there is no other method of obtaining the required information.
        Variable names that contain random letters and symbols followed by human-readable text may be internal IDs instead of actual names.
        If the user is requesting info on a project and didn't ask for you to look at the code, they probably want you to use query_id instead.
        If you get the output "project_token", please use the correct project ID. Null is not a valid input.
        :param id: A Scratch project ID as an integer, required argument.
        """

        a = loads(
            requests.get(
                "https://api.scratch.mit.edu/projects/"
                + urllib.parse.quote_plus(str(id))
                + "/"
            ).text
        )

        b = requests.get(
            "https://cdn.projects.scratch.mit.edu/"
            + urllib.parse.quote_plus(str(id))
            + "?token="
            + a["project_token"]
        ).text
        return b

    def query_project_sprites(self, id):
        """
        Obtain a list of all sprite names contained in a project with a given ID. Use this instead of query_project_json() where possible as this solution is faster and less confusing.

        :param id: A Scratch project ID as an integer, required argument.
        """
        a = loads(self.query_project_json(id))
        b = []
        for i in a["targets"]:
            b.append(i["name"])
        if b != "project_token":
            return b
        return "You typed the ID wrong. Ask the user to remind you of the correct ID."

    def query_sprite_variables(self, sprite, id):
        """
        Obtain a list of all variables contained in a sprite. Obtain the sprite's name first using query_project_sprites() if required.

        :param sprite: The name of the sprite in question as a string, required argument.
        :param id: The id of the project in question as an integer, required argument.
        """
        a = loads(self.query_project_json(id))
        b = {}  # processed variable JSON
        global c
        c = {}  # raw variable JSON
        for i in a["targets"]:
            if i["name"] == sprite:
                c = i["variables"]
                break
        for i in c.keys():
            b[c[i][0]] = c[i][1]
        if b != "project_token":
            return b
        return "You typed the ID wrong. Ask the user to remind you of the correct ID."

    def query_project_variables(self, id):
        """
        Obtain a list of all variables contained in a project.

        :param id: The id of the project in question as an integer, required argument.
        """
        a = loads(self.query_project_json(id))
        b = {}

        def get_sprite_variables(sprite, json_dict):
            x = json_dict
            y = {}  # processed variable JSON
            c = {}  # raw variable JSON
            for i in x["targets"]:
                if i["name"] == sprite:
                    c = i["variables"]
                    break
            for i in c.keys():
                y[c[i][0]] = c[i][1]
            return y

        for i in a["targets"]:
            b[i["name"]] = get_sprite_variables(i["name"], a)

        if b != "project_token":
            return b
        return "You typed the ID wrong. Ask the user to remind you of the correct ID."
