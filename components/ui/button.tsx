```tsx
import { Button as ButtonPrimitive } from '@base-ui/react/button'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
  [
    'inline-flex items-center justify-center gap-2',
    'whitespace-nowrap rounded-lg',
    'text-sm font-medium',
    'transition-all duration-200',
    'outline-none select-none',

    // Focus
    'focus-visible:ring-2',
    'focus-visible:ring-ring/50',
    'focus-visible:border-ring',

    // Disabled
    'disabled:pointer-events-none',
    'disabled:opacity-50',

    // Icons
    '[&_svg]:pointer-events-none',
    '[&_svg]:shrink-0',
    "[&_svg:not([class*='size-'])]:size-4",
  ].join(' '),

  {
    variants: {
      variant: {
        // Main EV action button
        default:
          'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90 hover:shadow-md',

        // Secondary actions
        secondary:
          'bg-secondary text-secondary-foreground hover:bg-secondary/80',

        // Buttons with visible border
        outline:
          'border border-border bg-background text-foreground hover:bg-muted',

        // Minimal navigation/action button
        ghost:
          'text-foreground hover:bg-muted hover:text-foreground',

        // Dangerous actions such as delete/remove
        destructive:
          'bg-destructive text-white shadow-sm hover:bg-destructive/90',

        // Text-link style
        link:
          'text-primary underline-offset-4 hover:underline',

        // EV-specific positive/action style
        success:
          'bg-emerald-600 text-white shadow-sm hover:bg-emerald-700',

        // EV charging/action style
        electric:
          'bg-cyan-600 text-white shadow-sm hover:bg-cyan-700',
      },

      size: {
        xs:
          'h-7 rounded-md px-2 text-xs',

        sm:
          'h-8 rounded-md px-3 text-sm',

        default:
          'h-10 px-4 py-2',

        lg:
          'h-11 rounded-xl px-6 text-base',

        xl:
          'h-12 rounded-xl px-8 text-base',

        icon:
          'size-10 p-0',

        'icon-sm':
          'size-8 p-0',

        'icon-lg':
          'size-12 p-0',
      },
    },

    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
)

function Button({
  className,
  variant = 'default',
  size = 'default',
  ...props
}: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) {
  return (
    <ButtonPrimitive
      data-slot="button"
      className={cn(
        buttonVariants({
          variant,
          size,
        }),
        className,
      )}
      {...props}
    />
  )
}

export { Button, buttonVariants }
```
