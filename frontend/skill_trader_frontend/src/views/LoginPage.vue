<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Login</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <ion-input v-model="username" label="Username" label-placement="stacked" required></ion-input>
      <ion-input v-model="password" label="Password" label-placement="stacked" required type="password"></ion-input>
      <ion-button expand="block" @click="handleLogin">Login</ion-button>
      <ion-text color="danger" v-if="error">{{ error }}</ion-text>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonInput, IonButton, IonText } from '@ionic/vue';
import { useRouter } from 'vue-router';
import { login } from '@/services/authService';

export default defineComponent({
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonInput,
    IonButton,
    IonText,
  },
  setup() {
    const username = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();

    const handleLogin = async () => {
      try {
        await login(username.value, password.value);
        router.push('/tabs/tab1'); // Redirect to main tab after login
      } catch (err) {
        error.value = 'Login failed. Please check your credentials.';
        console.error(err);
      }
    };

    return {
      username,
      password,
      error,
      handleLogin,
    };
  },
});
</script>
