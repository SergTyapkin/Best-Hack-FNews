import Vuex from 'vuex'
import Api from "./api.js";
import User from "../models/user";

const Store = new Vuex.Store({
  state: {
    user: new User(),
    api: new Api('/api'),
  },
  mutations: {
    SET_USER: (state, userData) => {
      state.user.set(userData);
    },
    SET_USER_CHOSENROOMID: (state, id) => {
      state.user.setChosenRoomId(id)
    },
    DELETE_USER: (state) => {
      state.user.setDefault();
    },
  },
  actions: {
    GET_USER: async (state, _) => {
      const userData = await state.state.api.getUser();
      if (userData.ok_)
        state.commit('SET_USER', userData);
      else
        state.commit('DELETE_USER');
    },
    DELETE_USER: async (state, _) => {
      state.commit('DELETE_USER');
    },
  }
});

export default Store;
