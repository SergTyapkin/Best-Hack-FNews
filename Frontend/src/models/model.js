export default class Model {
  default = {
  }
  toNetworkNames = {
  }

  setDefault(cls = this) {
    for (const key in cls.default) {
      this[key] = cls.default[key];
    }
  }

  constructor() {
    this.setDefault();
  }

  set(data, cls = this) {
    for (let key in cls.default) {
      if (this.default.hasOwnProperty(key)) {
        this[key] = data[key];
      }
    }
  }

  toNetwork() {
    const data = {};
    for (const key in this.toNetworkNames) {
      data[this.toNetworkNames[key]] = this[key];
    }
    return data;
  }
}
