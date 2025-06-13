<template>
  <nav
    class="sticky top-0 z-50 bg-gradient-to-r from-blue-800 to-indigo-900 shadow flex items-center px-6 py-1"
  >
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between py-4">
        <!-- Back Button -->
        <button
          class="text-white font-semibold mr-4 hover:underline focus:outline-none"
          @click="$router.push('/')"
        >
          ← Back to Home
        </button>

        <!-- Title -->
        <div class="hidden sm:flex sm:items-center">
          <h1 class="text-2xl font-bold text-white">Central Departmental Store</h1>
        </div>

        <!-- Profile and Cart -->
        <div class="hidden md:block">
          <div class="ml-4 flex items-center md:ml-6">
            <!-- Cart Button -->
            <button>
              <a
                href="#"
                class="bg-blue-100 text-black text-sm font-semibold px-4 py-2 rounded-lg mr-4 transition-colors duration-200 hover:bg-blue-500 hover:text-white active:bg-blue-700 active:text-white"
              >
                View Cart
              </a>
            </button>

            <!-- Profile dropdown -->
            <Menu as="div" class="relative ml-3">
              <div>
                <MenuButton class="flex items-center px-4 py-2 rounded-lg">
                  <img
                    class="size-12 rounded-full border-2 border-white transition-colors duration-200 hover:border-black"
                    :src="user.imageUrl"
                    alt=""
                  />
                </MenuButton>
              </div>
              <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <MenuItems
                  class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5 focus:outline-hidden"
                >
                  <p class="px-4 py-2 text-m text-gray-900">Hello {{ user.name }}!</p>

                  <MenuItem v-for="item in userNavigation" :key="item.name" v-slot="{ active }">
                    <a
                      :href="item.href"
                      :class="[
                        active ? 'bg-gray-100 outline-hidden' : '',
                        'block px-4 py-2 text-sm text-gray-700',
                      ]"
                      >{{ item.name }}</a
                    >
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'

const user = {
  name: 'Faiyaz Awsaf',
  email: 'faiyaz@gmail.com',
  imageUrl:
    'https://scontent.fdac14-1.fna.fbcdn.net/v/t39.30808-6/495450570_1847167692742618_6447877769157964880_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=yi4I216YRaQQ7kNvwG9ktOp&_nc_oc=Adn7ZYBXYhzFPEMghV6t4pl7q2Qf2sCSEAiWso_0MX95b62_g37Z5bvSBQMAz-AOKO0&_nc_zt=23&_nc_ht=scontent.fdac14-1.fna&_nc_gid=olRAND5OzPwEoDc19qKdSg&oh=00_AfPGSeJC41fqsMP86fziYnpBhFeBDcoNW6dXX-gZxGdUnw&oe=6851FD30',
}

const userNavigation = [
  { name: 'Your Profile', href: '#' },
  { name: 'Settings', href: '#' },
  { name: 'Sign out', href: '#' },
]
</script>
