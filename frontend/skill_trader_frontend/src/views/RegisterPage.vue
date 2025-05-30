<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Register</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <ion-input v-model="username" label="Username" label-placement="stacked" required></ion-input>
      <ion-input v-model="email" label="Email" label-placement="stacked" required type="email"></ion-input>
      <ion-input v-model="password" label="Password" label-placement="stacked" required type="password"></ion-input>
      <ion-button expand="block" @click="handleRegister">Register</ion-button>
      <ion-text color="danger" v-if="error">{{ error }}</ion-text>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonInput, IonButton, IonText } from '@ionic/vue';
import { useRouter } from 'vue-router';
import { registerUser } from '@/services/authService';

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
    const email = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();

    const handleRegister = async () => {
      try {
        await registerUser(username.value, password.value, email.value);
        router.push('/login'); // redirect to login after successful registration
      } catch (err) {
        error.value = 'Registration failed. Check your inputs.';
        console.error(err);
      }
    };

    return {
      username,
      email,
      password,
      error,
      handleRegister,
    };
  },
});
</script>
