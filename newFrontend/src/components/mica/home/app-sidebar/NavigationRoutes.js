export const navigationRoutes = {
  root: {
    name: '/',
    displayName: 'navigationRoutes.home',
  },
  routes: [
    {
      name: 'dashboard',
      displayName: 'menu.dashboard',
      meta: {
        iconClass: 'vuestic-iconset vuestic-iconset-dashboard',
      },
    },
    {
      name: 'my-house',
      displayName: 'menu.my-house',
      meta: {
        iconClass: 'font-awesome-iconset font-awesome-iconset-home',
      },
      disabled: false,
      children: [
        {
          name: 'add-transactions',
          displayName: 'menu.add-transactions',
          meta: {
            iconClass: 'font-awesome-iconset font-awesome-iconset-home',
          }
        },
        {
          name: 'shared-transactions',
          displayName: 'menu.shared-transactions',
          meta: {
            iconClass: 'font-awesome-iconset font-awesome-iconset-home',
          }
        },
        {
          name: 'analysis',
          displayName: 'menu.analysis',
          meta: {
            iconClass: 'vuestic-iconset vuestic-iconset-statistics',
          }
        },
        {
          name: 'rules',
          displayName: 'menu.rules',
          meta: {
            iconClass: 'vuestic-iconset vuestic-iconset-forms',
          }
        },
      ],
    },
    {
      name: 'settings',
      displayName: 'menu.settings',
      meta: {
        iconClass: 'vuestic-iconset vuestic-iconset-settings',
      },
      disabled: true,
      children: [
        {
          name: 'account',
          displayName: 'menu.account',
          meta: {
            iconClass: 'vuestic-iconset vuestic-iconset-settings',
          },
        },
        {
          name: 'consent',
          displayName: 'menu.consent',
          meta: {
            iconClass: 'vuestic-iconset vuestic-iconset-settings',
          },
        },
      ],
    },
  ],
}
