import Model from "./model";

export default class User extends Model {
  default = {
    id: '?',
    isLogined: false,
    username: "",
    password: "",
    email: "",
    name: "",
    role: "",
    balance: 0,
  }

  toNetworkNames = {
    username: "username",
    name: "name",
    email: "email",
    password: "password",
  }

  set(data) {
    super.set(data);
    this.isLogined = true;
  }

  constructor() {
    super();
    this.setDefault();
  }
}
