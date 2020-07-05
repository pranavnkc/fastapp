<template>
    <div>
        <nav v-if="currentUser" class="navbar navbar-expand navbar-dark bg-dark">
            <div class="navbar-nav">
                <router-link to="/" class="nav-item nav-link">Home</router-link>
                <router-link v-if="isAdmin" to="/create-service" class="nav-item nav-link">Create Service</router-link>
                <a @click="logout" class="nav-item nav-link">Logout</a>
            </div>
        </nav>
            <div class="container">
                <router-view></router-view>
            </div>
    </div>
</template>

<script>
import { authenticationService } from '@/_services';
import { router, Role } from '@/_helpers';

export default {
    name: 'app',
    data () {
        return {
            currentUser: null
        };
    },
    computed: {
        isAdmin () {
            console.log(this.currentUser, Role.ServiceProvider);
            return this.currentUser && this.currentUser.role === Role.ServiceProvider;
        }
    },
    created () {
        authenticationService.currentUser.subscribe(x => this.currentUser = x);
    },
    methods: {
        logout () {
            authenticationService.logout();
            router.push('/login');
        }
    }
};
</script>