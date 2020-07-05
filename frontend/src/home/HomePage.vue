<template>
    <span>
        <h1>List Of Services</h1>
        <div class="list-group" >
            <a href="#" class="list-group-item mb-1" v-for="service in services">
                <h4 class="list-group-item-heading">{{service.name}}</h4>
                <p class="list-group-item-text">{{service.description}}</p>
                <button type="button" v-if="currentUser.role=='client' && contactedServices.indexOf(service.id)==-1"@click="contactMe(service.id)" class="btn btn-primary">Contact Provider</button>
                <button type="button" v-if="currentUser.role=='client' && contactedServices.indexOf(service.id)!=-1" class="btn btn-success">Contacted</button>
                
            </a>
        </div>
</span>
</template>

<script>
import { authenticationService, serviceService } from '@/_services';

export default {
    data () {
        return {
            currentUser: authenticationService.currentUserValue,
            services: [],
            contactedServices:[],
        };
    },
    created () {
        serviceService.getServices().then(res => this.services = res.data);
    },
    methods: {
        contactMe(service_id){
            serviceService.contactServiceProvider(service_id).then(res=>{
                this.contactedServices.push(service_id);
            });
        }
    }
};
</script>