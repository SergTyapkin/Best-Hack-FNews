<template>
  <router-view></router-view>

  <Modal ref="modal"></Modal>
  <Popups ref="popups"></Popups>
</template>

<script>
import Modal from "../components/Modal.vue";
import Popups from "../components/Popups.vue";

export default {
  components: { Modal, Popups },

  mounted() {
    this.$store.state.modal = this.$refs.modal;
    this.$store.state.popups = this.$refs.popups;
  }
};
</script>
