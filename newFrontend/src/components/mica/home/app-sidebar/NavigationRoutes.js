export const navigationRoutes = {
  root: {
    name: '/',
    displayName: 'navigationRoutes.home',
  },
  routes: [
    {
      name: 'my-dashboard',
      displayName: 'menu.dashboard',
      meta: {
        iconClass: 'vuestic-iconset vuestic-iconset-dashboard',
      },
    },
    {
      name: 'my-house',
      displayName: 'menu.my-house',
      meta: {
        iconClass: 'fa fa-home',
      },
      disabled: true,
      children: [
        {
          name: 'shared-transactions',
          displayName: 'menu.shared-transactions',
        },
        {
          name: 'add-transactions',
          displayName: 'menu.add-transactions',
        },
        {
          name: 'noticeboard',
          displayName: 'menu.noticeboard',
        },
        {
          name: 'analysis',
          displayName: 'menu.analysis',
        },
        {
          name: 'rules',
          displayName: 'menu.rules',
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
