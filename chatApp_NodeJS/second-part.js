// pobranie modułu (include z c w nodejs)
var express = require('express');

//dołączanie modułu ORM 
const Sequelize = require('sequelize')

// dołączenie modułu usuwającego problem z zabezpieczeniem CORS
const cors = require('cors');

// dołączenie modułu obsługi sesji
var session = require('express-session')

// web soket
const WebSocket = require('ws');

//Inicjalizacja aplikacji
var app = express();
//process.env.PORT - pobranie portu z danych środowiska np. jeżeli aplikacja zostanie uruchomiona na zewnętrznej platformie np. heroku
var PORT = process.env.PORT || 8080;
//uruchomienie serwera
var server = app.listen(PORT,() => console.log(`Listening on ${ PORT }`));

const sequelize = new Sequelize('database', 'root', 'root', {
    dialect: 'sqlite',
    storage: 'orm-db.sqlite',
});

const sessionParser = session({
    saveUninitialized: false,
    secret: '$secret',
    resave: false
});

const wss = new WebSocket.Server({
    noServer: true,
});

// dołączenie modułu ułatwiającego przetwarzanie danych pochodzących z ciała zaytania HTTP (np. POST)
app.use(express.json());

// dołączenie modułu CORS do serwera
app.use(cors());

// dołączenie obslugi sesji do aplikacji 
app.use(sessionParser);


//dołączenie folderu public ze statycznymi plikami aplikacji klienckiej
app.use(express.static(__dirname + '/second-part/'));

// Stworzenie modelu - tabeli User
const User = sequelize.define('user', {
    user_id: {
      type: Sequelize.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    user_name: Sequelize.STRING,
    user_password: Sequelize.STRING
})


// synchroniznacja bazy danych - np. tworzenie tabel
sequelize.sync({ force: false }).then(() => {
  console.log(`Database & tables created!`)
})

// LISTA USERS ONLINE
let onlineUsers = {};

function testGet(request, response){
    response.send("testGet working");
}

// rejestrowanie użytkownika
function register(request, response) {
    console.log(request.body)
    var user_name = request.body.user_name;
    var user_password = request.body.user_password;
    if (user_name && user_password) {
        User.count({ where: { user_name: user_name } }).then(
            count => {
                if (count != 0) {
                    response.send({ register: false });
                } else {
                    User.create({user_name: user_name, user_password: user_password})
                        .then(() => response.send({ register: true }))
                        .catch(function (err) { response.send({ register: true })
                      });
                }
            })
    } else {
        response.send({ register: false });
    }
}

// logowanie uzytkownika
function login(request, response) {
    console.log(request.body)
    var user_name = request.body.user_name;
    var user_password = request.body.user_password;
    if (user_name && user_password) {
        User.count({ where: { user_name: user_name, user_password: user_password } }).then(
            count => {
                if (count != 0) {
                    User.findAll({
                        attributes: ['user_id'],
                        where:{
                            user_name: user_name,
                            user_password: user_password
                        }
                    }).then(users => {
                        request.session.loggedin = true;
                        request.session.user_id = users[0].user_id;
                        //console.log(request.session.user_id)
                        response.send({ loggedin: request.session.loggedin });
                    })
                } else {
                    response.send({ loggedin: false });
                }
            })
    } else {
        response.send({ loggedin: false });
    }
}

// sprawdzenie logowania jeżeli funkcja checkSessions nie zwróci błędu
function loginTest(request, response) {
    response.send({ loggedin: true });
}

function logout(request, response) {
    console.log("logout")
    request.session.destroy();
    response.send({ loggedin: false });
}

function checkSessions(request, response, next) {
    if (request.session.loggedin) {
        next();
    } else {
        response.send({ loggedin: false });
    }
}

function getUsers(request, response) {
    var data = {data:[]};
    User.findAll({
        attributes: ['user_id','user_name'],
    }).then(users => {
        users.forEach(user => {
            var online = false
            //console.log(onlineUsers)
            if(user.dataValues.user_id in onlineUsers) {
                online = true;
            }
            data.data.push({
                user_id: user.dataValues.user_id,
                user_name: user.dataValues.user_name,
                online: online
            })
        });
        response.send(data);
    })
}

app.get('/api/test-get', testGet);

app.post('/api/register/', [register]);

app.post('/api/login/', [login]);

app.get('/api/login-test/', [checkSessions, loginTest]);

app.get('/api/logout/', [checkSessions, logout]);

app.get('/api/users/', [checkSessions, getUsers]);

server.on('upgrade', function (request, socket, head) {
    // Sprawdzenie czy dla danego połączenia istnieje sesja
    sessionParser(request, {}, () => {
        if (!request.session.user_id) {
            socket.destroy();
            return;
        }
        wss.handleUpgrade(request, socket, head, function (ws) {
            wss.emit('connection', ws, request);
        });
    });
});

wss.on('connection', function (ws, request) {

    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ status: 2 }));
        }
    });
    onlineUsers[request.session.user_id] = ws;

    ws.on('message', function (message) {
        console.log(String(message))
        // parsowanie wiadomosci z JSONa na obiekt
        try {
            var data = JSON.parse(message);
        } catch (error) {
            return;
        }
    });

    ws.on('close', () => {
        delete onlineUsers[request.session.user_id];
    })

});



// W funkcji pobierania użytkowników warto wykorzystać podany kod do 
// przemapowania obiektów bazy danych na obiekty JSON
//users = users.map(user => {
//        return user.toJSON();
//});
            
// Przejscia po obiektach w liście obiektów i dodanie w nich odpowiedniego pola
//for (user of users) {
//    user.online = true;
//}
