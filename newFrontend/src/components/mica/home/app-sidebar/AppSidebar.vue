<template>
  <aside
    class="app-sidebar"
    :class="computedClass"
    :style="computedStyle"
  >
    <ul class="app-sidebar__menu">
      <template v-for="(item, key) in items">
        <app-sidebar-link-group
          :key="key"
          :minimized="minimized"
          :icon="item.meta && item.meta.iconClass"
          v-if="item.children"
          :title="$t(item.displayName)"
          :children="item.children"
          :active-by-default="hasActiveByDefault(item)"
        >
          <app-sidebar-link
            v-for="(subMenuItem, key) in item.children"
            :key="key"
            :to="{ name: subMenuItem.name }"
            :title="$t(subMenuItem.displayName)"
          />
        </app-sidebar-link-group>
        <app-sidebar-link
          v-else
          :key="key"
          :minimized="minimized"
          :active-by-default="item.name === $route.name"
          :icon="item.meta && item.meta.iconClass"
          :to="{ name: item.name }"
          :title="$t(item.displayName)"
        />
      </template>
        <app-sidebar-link-group
          :minimized="minimized"
          :active-by-default="true"
          :children="[]"
          icon="fa fa-question"
          title="Help"
        >
          <app-sidebar-link
            :title="helpInstructions()"
            :active-by-default="true"
          >
          </app-sidebar-link>
        </app-sidebar-link-group>
    </ul>
  </aside>
</template>

<script>
import { navigationRoutes } from './NavigationRoutes'
import AppSidebarLink from './components/AppSidebarLink'
import AppSidebarLinkGroup from './components/AppSidebarLinkGroup'
import { ColorThemeMixin } from '../../../../services/vuestic-ui'

export default {
  name: 'app-sidebar',
  inject: ['contextConfig'],
  components: {
    AppSidebarLink,
    AppSidebarLinkGroup,
  },
  mixins: [ColorThemeMixin],
  props: {
    minimized: {
      type: Boolean,
      required: true,
    },
    color: {
      type: String,
      default: 'secondary',
    },
  },
  data () {
    return {
      items: navigationRoutes.routes,
    }
  },
  computed: {
    computedClass () {
      return {
        'app-sidebar--minimized': this.minimized,
      }
    },
    computedStyle () {
      return {
        backgroundColor: this.contextConfig.invertedColor ? 'white' : this.colorComputed,
      }
    },
  },
  methods: {
    hasActiveByDefault (item) {
      return item.children.some(child => child.name === this.$route.name)
    },
    helpInstructions() {
      switch (this.$route.name){
        case 'add-transactions':
          return "This is a list of your personal banking transactions. Quickly add them to your shared household expenses. These have been taken straight from your bank and are not retained unless added to your shared payments."
          break
        case 'noticeboard':
          return "Conveniently message others in your household about pressing matters."
          break
        case 'analytics':
          return "View a breakdown of your payments. Use this information to better budget."
          break
        case 'rules':
          return "Set and view agreed on rules with your housemates. This will make the boundaries of your arrangement clear and manageable."
          break
        case 'shared-transactions':
          return "This is a list of the payments shared in your house. Check your balance, and settle your debts."
          break
        default:
          return "Welcome to Mica! This is your one-stop-shop for convenient household financial management, as well as helping you with your budgeting."
      }
    }
  },
}

</script>

<style lang="scss">
.app-sidebar {
  overflow: auto;
  display: flex;
  max-height: 100%;
  flex: 0 0 16rem;

  @include media-breakpoint-down(sm) {
    flex: 0 0 100%;
  }

  &--minimized {
    flex: 0 0 3.25rem;
  }

  &__menu {
    margin-bottom: 0;
    padding-top: 2.5625rem;
    padding-bottom: 2.5rem;
    list-style: none;
    padding-left: 0;
    width: 100%;
  }
}
</style>
