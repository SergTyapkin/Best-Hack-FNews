import ApiRequest from "../utils/requests";

export default class Api extends ApiRequest {
    signUp = (username, email, password, fullname) => this.post('/users', {username, email, password, fullname});
    signIn = (username, password) => this.post('/user/auth', {username, password});
    getUser = () => /*{
        return {
            ok_: true,
            username: 'serg',
            email: 'some@mail.ru',
            name: 'Сергей',
        }
    }*/this.get('/user');
    updateUser = ({username, email, fullname}) => this.put('/user', {username, email, fullname});
    signOut = () => this.delete('/user/session');
    updatePassword = (oldPassword, newPassword) => this.put('/user/password', {oldPassword, newPassword});

    getHistory = () => /*{
        return {
            ok_: true,
            actions: [{action: 'topup', message: '+ 2150 €', date: 'timestamp'}, {action: 'withdraw', message: '- 100 $', date: 'timestamp'}]
        };
    }*/this.get('/history');
    getUserBalance = () => /*{
        return {
            ok_: true,
            currencies: [
                {name: 'uah', value: 10},
                {name: 'krw', value: 1120.4},
                {name: 'usd', value: 0.632},
            ],
        }
    }*/this.get('/balance/currencies');

    getCurrencies = () => /*{
        return {
            ok_: true,
            currencies: [
                {name: "EUR", value: '88', percents: '3.35'},
                {name: "KZT", value: '7.3', percents: '2.8'},
                {name: "XDR", value: '34.3', percents: '-6.40'},
                {name: "TRY", value: '3324.3', percents: '-2.40'},
                {name: "INR", value: '398.2', percents: '-9.40'},
            ]
        }
    }*/this.get('/currencies');

    doExchange = ({nameFrom, nameTo, valueTo}) => this.put('/exchange', {nameFrom, nameTo, valueTo});
}
