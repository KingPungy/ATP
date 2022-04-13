.cpu cortex-m0
.align 2

.data

LIT0: .asciz "=======[Begin]======="
LIT1: .asciz "test"
LIT2: .asciz "=======[End]======="

.text
.global ScolangMain

ScolangMain:
push { r4, lr }
ldr r0, =LIT0
bl smartPrint
@definition of fibonacci was performed
@definition of even was performed
@definition of odd was performed
@definition of multi was performed
@definition of sommig was performed
@definition of greater was performed
@definition of power was performed
@definition of divF was performed
@definition of add was performed
@definition of subtract was performed
mov r4, #12
mov r0, r4
mov r1, #9
bl divide
mov r4, r0
mov r0, r4
bl smartPrint
ldr r0, =LIT1
bl smartPrint
ldr r0, =LIT2
bl smartPrint
pop { r4, pc }
