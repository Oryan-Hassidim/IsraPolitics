import { esbuildPlugin } from '@web/dev-server-esbuild';

export default /**@type{import('@web/dev-server').DevServerConfig}*/({
  nodeResolve: true,
  plugins: [esbuildPlugin({
    ts: true,
    target: 'es2022',
    tsconfig: 'tsconfig.json',
  })],
});