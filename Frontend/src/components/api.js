import ApiRequest from "../utils/requests";

export default class Api extends ApiRequest {
    signUp = (username, email, password, name) => this.post('/user', {
        new_user: {
            username: username,
            email: email,
            password: password,
            name: name
        }
    });
    isLogined = false;
    signIn = (username, password) => {
        this.isLogined = true;
        return {
            ok_: true,
        }
    }/*this.post('/user/login/token', {
        form_data: {username, password}
    });*/
    getUser = () => {
        const userData =  {
            ok_: true,
            username: 'serg',
            email: 'some@mail.ru',
            name: 'Сергей',
        };
        if (!this.isLogined)
            userData.ok_ = false;
        return userData;
    }//this.get('/user');
    updateUser = ({username, email, name}) => this.put('/user', {username, email, name});
    signOut = () => {
        this.isLogined = false;
        return {
            ok_: true,
        }
    }//this.delete('/user/session');
    updatePassword = (oldPassword, newPassword) => this.put('/user/password', {oldPassword, newPassword});

    getHistory = () => {
        return {
            ok_: true,
            actions: [{action: 'topup', message: '+ 2150 €', date: 'timestamp'}, {action: 'withdraw', message: '- 100 $', date: 'timestamp'}]
        };
    }//this.get('/history');
    getUserBalance = () => {
        return {
            ok_: true,
            currencies: [
                {name: 'uah', amount: 10},
                {name: 'krw', amount: 1120.4},
                {name: 'usd', amount: 0.632},
            ],
        }
    }//this.get('/wallet/currencies');

    getCurrencies = () => {
        return {
            ok_: true,
            currencies: [
                {name: "EUR", amount: '88'},
                {name: "KZT", amount: '7.3'},
                {name: "XDR", amount: '34.3'},
                {name: "TRY", amount: '3324.3'},
                {name: "INR", amount: '398.2'},
            ]
        }
    }//this.get('/wallet/currencies');
    getWatchingCurrencies = () => {
        return {
            ok_: true,
            currencies: [
                {name: "EUR", rate: '88', percents: '3.35'},
                {name: "KZT", rate: '7.3', percents: '2.8'},
                {name: "XDR", rate: '34.3', percents: '-6.40'},
                {name: "TRY", rate: '3324.3', percents: '-2.40'},
                {name: "INR", rate: '398.2', percents: '-9.40'},
            ]
        }
    }//this.get('/wallet/currencies');
    getAllCurrencies = () => {
        return {
            ok_: true,
            currencies: [
                {name: "AUD", rate: '88', percents: '3.35'},
                {name: "AZN", rate: '88', percents: '3.35'},
                {name: "GBP", rate: '88', percents: '3.35'},
                {name: "AMD", rate: '88', percents: '3.35'},
                {name: "BYN", rate: '88', percents: '3.35'},
                {name: "BRL", rate: '88', percents: '3.35'},
                {name: "HUF", rate: '88', percents: '3.35'},
                {name: "HKD", rate: '88', percents: '3.35'},
                {name: "DKK", rate: '7.3', percents: '2.8'},
                {name: "USD", rate: '34.3', percents: '-6.40'},
                {name: "EUR", rate: '34.3', percents: '-6.40'},
                {name: "INR", rate: '34.3', percents: '-6.40'},
                {name: "KZT", rate: '34.3', percents: '-6.40'},
                {name: "CAD", rate: '34.3', percents: '-6.40'},
                {name: "KGS", rate: '3324.3', percents: '-2.40'},
                {name: "CNY", rate: '398.2', percents: '-9.40'},
                {name: "MDL", rate: '398.2', percents: '-9.40'},
                {name: "NOK", rate: '398.2', percents: '-9.40'},
                {name: "PLN", rate: '398.2', percents: '-9.40'},
                {name: "RON", rate: '398.2', percents: '-9.40'},
                {name: "XDR", rate: '398.2', percents: '-9.40'},
                {name: "SGD", rate: '398.2', percents: '-9.40'},
                {name: "TJS", rate: '398.2', percents: '-9.40'},
                {name: "TRY", rate: '398.2', percents: '-9.40'},
                {name: "TMT", rate: '398.2', percents: '-9.40'},
                {name: "UZS", rate: '398.2', percents: '-9.40'},
                {name: "UAH", rate: '398.2', percents: '-9.40'},
                {name: "CZK", rate: '398.2', percents: '-9.40'},
                {name: "SEK", rate: '398.2', percents: '-9.40'},
                {name: "CHF", rate: '398.2', percents: '-9.40'},
                {name: "ZAR", rate: '398.2', percents: '-9.40'},
                {name: "KRW", rate: '398.2', percents: '-9.40'},
                {name: "JPY", rate: '398.2', percents: '-9.40'},
                {name: "RUB", rate: '1', percents: '0'},
            ]
        }//this.get('/wallet/currencies/all');
    }

    getNews = () => {
        return {
            ok_: true,
            news: [
                {title: 'Технологии электронного носа помогут различать виски',
                    date: '12.04.2022',
                    source: 'RussiaToday',
                    description: 'Исследователи из Технологического университета Сиднея в Австралии разработали NOS.E, устройство, которое может найти различия между виски, «нюхая» их.\n' +
                      '\n' +
                      'Опытные любители виски считают, что они могут почувствовать разницу, вкус и запах между первоклассными спиртными напитками и дешевым «суррогатом». Но даже самые искушенные ценители все равно могут стать жертвами мошенничества, которое, вы наверное и не знали, становится растущей проблемой для индустрии виски.',
                tags: ['кулинария']},
                {title: 'Технологии электронного носа помогут различать виски',
                    date: '12.04.2022',
                    source: 'RussiaToday',
                    description: 'Исследователи из Технологического университета Сиднея в Австралии разработали NOS.E, устройство, которое может найти различия между виски, «нюхая» их.\n' +
                      '\n' +
                      'Опытные любители виски считают, что они могут почувствовать разницу, вкус и запах между первоклассными спиртными напитками и дешевым «суррогатом». Но даже самые искушенные ценители все равно могут стать жертвами мошенничества, которое, вы наверное и не знали, становится растущей проблемой для индустрии виски.',
                    tags: ['Кулинария']},
                {title: 'Технологии электронного носа помогут различать виски',
                    date: '12.04.2022',
                    source: 'RussiaToday',
                    description: 'Исследователи из Технологического университета Сиднея в Австралии разработали NOS.E, устройство, которое может найти различия между виски, «нюхая» их.\n' +
                      '\n' +
                      'Опытные любители виски считают, что они могут почувствовать разницу, вкус и запах между первоклассными спиртными напитками и дешевым «суррогатом». Но даже самые искушенные ценители все равно могут стать жертвами мошенничества, которое, вы наверное и не знали, становится растущей проблемой для индустрии виски.',
                    tags: ['Финансы']},
                {title: 'Технологии электронного носа помогут различать виски',
                    date: '12.04.2022',
                    source: 'RussiaToday',
                    description: 'Исследователи из Технологического университета Сиднея в Австралии разработали NOS.E, устройство, которое может найти различия между виски, «нюхая» их.\n' +
                      '\n' +
                      'Опытные любители виски считают, что они могут почувствовать разницу, вкус и запах между первоклассными спиртными напитками и дешевым «суррогатом». Но даже самые искушенные ценители все равно могут стать жертвами мошенничества, которое, вы наверное и не знали, становится растущей проблемой для индустрии виски.',
                    tags: ['Политика', 'Технологии']},
                {title: 'Технологии электронного носа помогут различать виски',
                    date: '12.04.2022',
                    source: 'RussiaToday',
                    description: 'Исследователи из Технологического университета Сиднея в Австралии разработали NOS.E, устройство, которое может найти различия между виски, «нюхая» их.\n' +
                      '\n' +
                      'Опытные любители виски считают, что они могут почувствовать разницу, вкус и запах между первоклассными спиртными напитками и дешевым «суррогатом». Но даже самые искушенные ценители все равно могут стать жертвами мошенничества, которое, вы наверное и не знали, становится растущей проблемой для индустрии виски.',
                    tags: []},
            ]
        }
    }//this.get('/news');

    doExchange = ({nameFrom, nameTo, valueTo, valueFrom}) => this.post('/wallet/exchange', {nameFrom, nameTo, valueTo, valueFrom});

    addCurrency = (name) => this.post('/wallet/currency', {name});
    removeCurrency = (name) => this.delete('/wallet/currency', {name});

    topup = (value) => this.post('/wallet/topup', {currency: {name: "RUB", amount: value}});
    withdraw = (value) => this.post('/wallet/withdraw', {currency: {name: "RUB", amount: value}});

    getTopics = () => {
        return {
            ok_: true,
            topics: [
                {id: 56, name: 'Кулинария', keys: "Молоко, яйца, мука, хлеб, дрожжи", author: 'serg'},
                {id: 12, name: 'Строительство', keys: "Молоко, яйца, мука, хлеб, дрожжи", author: 'Username42'},
                {id: 100, name: 'Финансы', keys: "Молоко, яйца, мука, хлеб, дрожжи", author: 'User61'},
            ]
        };
    }//this.get('/topics');
    createTopic = (name, keys) => this.post('/topics', {name, keys});
    deleteTopic = (id) => this.delete('/topics', {id});
    updateTopic = (id, name, keys) => this.put('/topics', {id, name, keys});
}
