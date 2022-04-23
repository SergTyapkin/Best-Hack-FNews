import ApiRequest from "../utils/requests";

export default class Api extends ApiRequest {
    signUp = (username, email, password, fullname) => this.post('/users', {username, email, password, fullname});
    signIn = (username, password) => this.post('/user/auth', {username, password});
    getUser = () => {
        return {
            ok_: true,
            username: 'serg',
            email: 'some@mail.ru',
            name: 'Сергей',
        }
    }//this.get('/user');
    updateUser = ({username, email, fullname}) => this.put('/user', {username, email, fullname});
    signOut = () => this.delete('/user/session');
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
                {name: 'uah', value: 10},
                {name: 'krw', value: 1120.4},
                {name: 'usd', value: 0.632},
            ],
        }
    }//this.get('/balance/currencies');
}
