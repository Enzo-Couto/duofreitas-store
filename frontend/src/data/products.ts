import camisetaFrente from '@/assets/images/products/shirt1/shirt-person-front.png'
import camisetaCostas from '@/assets/images/products/shirt1/shirt-person-back.png'

export const products = [
  {
    id: 1,
    slug: 'camiseta-duo-freitas',
    name: 'Camiseta Duo Freitas',
    price: 89.9,
    category: 'feminino',
    frontImage: camisetaFrente,
    backImage: camisetaCostas,
    description: 'Camiseta premium confeccionada em algodão.',
    sizes: ['P', 'M', 'G', 'GG'],
  },
  {
    id: 2,
    slug: 'camiseta-duo-freitas-premium',
    name: 'Camiseta Duo Freitas Premium',
    price: 99.9,
    category: 'premium',
    frontImage: camisetaFrente,
    backImage: camisetaCostas,
    description: 'Versão premium da coleção.',
    sizes: ['P', 'M', 'G', 'GG'],
  },
]
