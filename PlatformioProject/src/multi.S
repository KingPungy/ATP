.cpu cortex-m0
.align 2

.text
.global multi

multi:
push { r4, r5, r6, lr }
mov r4, r0
mov r5, r1
mul r4, r4, r5
mov r6, r4
mov r0, r6
pop { r4, r5, r6, pc }
