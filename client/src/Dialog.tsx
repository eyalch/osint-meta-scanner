import { ReactNode, forwardRef, useImperativeHandle, useRef } from "react"

interface DialogProps {
  children: ReactNode
}

export interface DialogRef {
  showModal: () => void
  close: () => void
}

export default forwardRef<DialogRef, DialogProps>(function Dialog(props, ref) {
  const dialogRef = useRef<HTMLDialogElement>(null)

  useImperativeHandle(ref, () => ({
    showModal: () => dialogRef.current?.showModal(),
    close: () => dialogRef.current?.close(),
  }))

  return (
    <dialog
      ref={dialogRef}
      onClick={(event) => {
        if (event.target === dialogRef.current) {
          dialogRef.current.close()
        }
      }}
    >
      {props.children}
    </dialog>
  )
})
