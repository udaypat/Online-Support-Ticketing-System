<template>
    <NavBar></NavBar>

    <div class="container mt-4">
        <h1>Frequently Asked Questions</h1>
        <div class="media justify-content-end" v-for="(faq, index) in faq_list" :key="index">
            <!-- <div class="media-body text-right">
                <h5 class="mt-0">{{ faq.query }}
                </h5>
                <p>
                    {{ faq.answer }}
                </p>
            </div>
            <hr> -->

            <div class="accordion accordion-flush" id="accordionFlushExample">
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            :data-bs-target="'#collapseOne' + index" aria-expanded="false" aria-controls="">
                            {{ faq.query }}
                        </button>
                    </h2>
                    <div :id="'collapseOne' + index" class="accordion-collapse collapse"
                        data-bs-parent="#accordionFlushExample">
                        <div class="accordion-body">{{ faq.answer }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import config from "@/config.js";
import NavBar from '@/components/NavBar.vue';

export default {
    components: {
        NavBar,
    },
    name: "FAQs",
    data() {
        return {
            faq_list: [],
        }
    },
    methods: {
        Get_FAQ_list() {
            // Get list of FAQs
            fetch(`${config.BASE_API_URL}/faqs`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.faq_list = res
                    console.log("got faq list")
                    console.log(this.faq_list)

                });
        },
    },
    created() {
        this.Get_FAQ_list()
    }
};

</script>


<style></style>