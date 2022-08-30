# Shortener Application

This is url shortener application like [bitly](https://bitly.com/ "https://bitly.com/").


### Technology Stack

---

**Backend:** Python (FASTApi)

**Database:** SQLLite

**Devops:** Docker

Protocol: REST


### How to Run

---

After clonning the repo and install [docker](https://docs.docker.com/engine/install/ "https://docs.docker.com/engine/install/") and [docker-compose](https://docs.docker.com/compose/install/ "https://docs.docker.com/compose/install/") just type `docker-compose up`  in the destination where Dockerfile in.


### Endpoints

---

Project has swagger support. So that you can directly see from `http://localhost:8000/docs` .

| URL        | METHOD | Request           | Action     |
| ---------- | ------ | ----------------- | ---------- |
| /url       | GET    |                   | List URLs  |
| /url       | POST   | target_url (JSON) | Create URL |
| /{url_key} | GET    | url_key (param)   | Forwarding |


### Wanna be a contributor?
---

Please follow the tips [here](https://github.com/selvianl/url_shortener/blob/main/CONTRIBUTING.md)
